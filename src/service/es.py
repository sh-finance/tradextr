import config

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

# from langchain_core.documents import Document
# es_vector_store.add_documents(
#   documents=[
#     Document(page_content="123123123", metadata = { "url": "https://example.com", "html": "<html></html>" }),
#     Document(page_content="456456456", metadata = { "url": "https://example.com", "html": "<html></html>" }),
#   ]
# )


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
