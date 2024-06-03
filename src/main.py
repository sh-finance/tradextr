from logger import logger
from fastapi import FastAPI

api = FastAPI()


@api.get("/health")
def health():
    return {"code": 0, "message": "ok"}


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
