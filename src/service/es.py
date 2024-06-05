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


def search(query: str) -> list[Context]:
    docs = es_vector_store.similarity_search(query)
    return [
        Context(
            content=doc.page_content,
            link=doc.metadata["url"],
            title=doc.metadata["title"],
        )
        for doc in docs
    ]


if not es.indices.exists(index=config.Elasticsearch.index_name):
    es.indices.create(index=config.Elasticsearch.index_name)
