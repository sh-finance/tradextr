import config

import json

from dto.entity.context import (
    filter_contexts,
    generate_markdown_references,
    sort_contexts,
)
from dto.entity.response import ParrotResponse
from logger import logger
from fastapi import FastAPI, Request

from util.extractor import extract_date_range
from util.reformulate_as_separate_question import reformulate_as_separate_question
from util.rag import rag

from service.tavily import search as tavily_search
from service.es import search as es_search

api = FastAPI()


@api.get("/health")
def health():
    return {"code": 0, "message": "ok"}


@api.post("/biodiesel-trader/rag")
async def rag_handler(request: Request):
    try:
        dto = await request.json()
    except Exception as e:
        return ParrotResponse(str(e), "error")

    logger.info("dto: %s", dto)

    messages = dto.get("messages", [])

    if len(messages) == 0:
        return ParrotResponse("empty messages", "error")

    # 取最后一句话为用户问题
    query = messages[-1]
    query_with_context = query.get("content")
    history = messages[0:-1]

    if query.get("role") != "user":
        return ParrotResponse("last message is not user's question", "error")

    if len(history) > 0:
        query_with_context = reformulate_as_separate_question(messages)

    logger.info("query_with_context: %s", query_with_context)

    contexts = []

    date_range = extract_date_range(query=query_with_context)

    contexts = es_search(query_with_context, startDate=date_range.start)

    # if len(contexts) < config.Tavily.max_results:
    tavily_results = tavily_search(query_with_context, news=bool(date_range.start))
    contexts.extend(tavily_results)
    contexts = sort_contexts(contexts)
    contexts = filter_contexts(contexts)
    # logger.info("\n".join([context.__str__() for context in contexts]))
    logger.info("\n".join([json.dumps(context.__dict__()) for context in contexts]))

    answer = rag(json.dumps(messages), contexts)

    ref = generate_markdown_references(contexts)

    return ParrotResponse(
        answer + "\n\n" + ref,
        metadata={
            "query_with_context": query_with_context,
            "contexts": [ctx.__str__() for ctx in contexts],
        },
    )


if __name__ == "__main__":
    import uvicorn
    # from schedule import scheduler_run

    # if config.Server.mode == "prod":
    #     scheduler_run()

    logger.debug(config)

    uvicorn.run(
        app=config.Server.app,
        host=config.Server.host,
        port=config.Server.port,
        reload=config.Server.reload,
        reload_includes=config.Server.reload_includes,
        reload_excludes=config.Server.reload_excludes,
        reload_delay=config.Server.reload_delay,
    )
