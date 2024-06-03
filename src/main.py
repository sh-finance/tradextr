from logger import logger
from fastapi import FastAPI

api = FastAPI()


@api.get("/health")
def health():
    return {"code": 0, "message": "ok"}


if __name__ == "__main__":
    import uvicorn
    from config import Server

    uvicorn.run(
        app=Server.app,
        host=Server.host,
        port=Server.port,
        reload=Server.reload,
    )
