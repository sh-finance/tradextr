from typing import List, Optional, cast

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from service.openai import llm
from util.today import today


class KeywordsData(BaseModel):
    """Keywords in a sentence"""

    keywords: Optional[List[str]] = Field(
        default=[], description="Keywords in a sentence"
    )


class DateRange(BaseModel):
    """Date Range in a sentence, return None if not specified."""

    start: Optional[str] = Field(description="the start of date range")
    end: Optional[str] = Field(description="the end of date range")


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        # Please see the how-to about improving performance with
        # reference examples.
        # MessagesPlaceholder('examples'),
        ("human", "{query}"),
    ]
)

keywords_extractor = prompt | llm.with_structured_output(schema=KeywordsData)

date_range_extractor = prompt | llm.with_structured_output(schema=DateRange)


def extract_keyword(query: str):
    res = keywords_extractor.invoke({"query": query})
    return cast(KeywordsData, res).keywords


def extract_date_range(query: str):
    res = date_range_extractor.invoke({"query": f"{query}\ncurrent date is {today()}"})
    return cast(DateRange, res)
