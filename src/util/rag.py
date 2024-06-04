from datetime import date

from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser

from logger import logger

from dto.entity.context import Context

from service.openai import llm

from util.extractor import keywords_extractor

prompt_template = open("prompt/rag.md", "r").read()

prompt = PromptTemplate.from_template(prompt_template)

chain = prompt | llm | StrOutputParser()


def rag(messages: str, contexts: list[Context]):
    context_str = "\n".join([ctx.__xml__() for ctx in contexts])

    answer = chain.invoke(
        {
            "messages": messages,
            "context": context_str,
            "current_date": date.today().isoformat(),
        }
    )

    return answer
