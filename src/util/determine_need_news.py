from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from service.openai import llm


class Answer(BaseModel):
    need_news: bool = Field(description="determine if news is needed as context")


parser = JsonOutputParser(pydantic_object=Answer)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser


def determine_need_news(query: str):
    answer = chain.invoke({"query": query})
    return answer["need_news"]
