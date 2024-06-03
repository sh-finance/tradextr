from logger import logger
from fastapi import FastAPI

api = FastAPI()


@api.get("/")
def test():
    logger.info("test")
    return "hello"


if __name__ == "__main__":
    import uvicorn
    from config import Server

    uvicorn.run(
        app=Server.app,
        host=Server.host,
        port=Server.port,
    )
