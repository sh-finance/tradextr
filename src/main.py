from dto.entity.response import ParrotResponse
from logger import logger
from fastapi import FastAPI, Request

from util.reformulate_as_separate_question import reformulate_as_separate_question
from util.rag import rag


api = FastAPI()


@api.get("/health")
def health():
    return {"code": 0, "message": "ok"}


@api.post("/rag")
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
    context = messages[0:-1]

    if query.get("role") != "user":
        return ParrotResponse("last message is not user's question", "error")

    if len(context) > 0:
        query = reformulate_as_separate_question(query.get("content"), context)

    logger.info("query: %s", query)

    answer = rag(query, contexts=[])

    return ParrotResponse(answer)


if __name__ == "__main__":
    import uvicorn
    import config

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
