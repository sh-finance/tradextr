from typing import Any
import config

from tavily import TavilyClient
from langchain_community.tools.tavily_search import TavilySearchResults, TavilyAnswer
from openai.types.chat import ChatCompletionMessageParam
from util.reformulate_as_separate_question import reformulate_as_separate_question

tavily_client = TavilyClient(config.Tavily.api_key())
# tavily_search = TavilySearchResults(max_results=config.Tavily.max_results)
# tavily_answer = TavilyAnswer()


class TavilySearchResult:
    title: str
    url: str
    content: str
    score: float
    raw_content: str | None


class TavilySearchResponse:
    query: str
    follow_up_questions: str | None
    answer: str | None
    images: list[str] | None
    results: list[TavilySearchResult]
    response_time: float


def search(query: str, domains: list[str] = []):
    # res: TavilySearchResponse | None = tavily_client.search(query=query, search_depth = "advanced", max_results = config.Tavily.max_results, include_domains = domains)
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=config.Tavily.max_results,
        include_domains=domains,
    )
    results = response and response.get("results", []) or []
    return [
        {
            "title": res.get("title"),
            "content": res.get("content"),
            "url": res.get("url"),
        }
        for res in results
        if res.get("content")
    ]


def qna_with_context(history: list[ChatCompletionMessageParam] | Any = []):
    question = history[-1].get("content", "")
    if not question:
        return "", []
    query = reformulate_as_separate_question(
        question=str(question), history=history[:-1]
    )
    res = tavily_client.search(
        query=query, include_answer=True, max_results=config.Tavily.max_results
    )
    if res:
        return res.get("answer", ""), res.get("results", [])
    return "", []
