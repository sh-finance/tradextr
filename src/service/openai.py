import config

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

llm = ChatOpenAI(model=config.OpenAI.model, temperature=0)
embedding = OpenAIEmbeddings(model=config.OpenAI.embedding_model)
