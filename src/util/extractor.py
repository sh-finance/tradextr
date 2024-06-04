from typing import List, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from service.openai import llm


class KeywordsData(BaseModel):
    """Keywords in a sentence"""

    keywords: Optional[List[str]] = Field(
        default=[], description="Keywords in a sentence"
    )


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
        ("human", "{text}"),
    ]
)

keywords_extractor = prompt | llm.with_structured_output(schema=KeywordsData)
