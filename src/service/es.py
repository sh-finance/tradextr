import config

from typing import List
from langchain_core.documents import Document

from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore

from dto.entity.context import Context

from service.openai import embedding

es = Elasticsearch(config.Elasticsearch.url)

es_vector_store = ElasticsearchStore(
    embedding=embedding,
    index_name=config.Elasticsearch.index_name,
    es_connection=es,
)

mappings = {
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "vector": {"type": "dense_vector"},
            "metadata": {
                "type": "nested",
                "properties": {
                    "url": {"type": "keyword"},
                    "html": {"type": "text"},
                    "title": {"type": "text"},
                    "date": {"type": "date"},
                },
            },
        }
    }
}

if not es.indices.exists(index=config.Elasticsearch.index_name):
    es.indices.create(index=config.Elasticsearch.index_name, body=mappings)


def search(query: str, k: int = config.Tavily.max_results) -> list[Context]:
    tuples = es_vector_store.similarity_search_with_relevance_scores(query=query, k=k)

    return [
        Context(
            content=doc.page_content,
            link=doc.metadata["url"],
            title=doc.metadata["title"],
            score=score,
        )
        for doc, score in tuples
    ]
