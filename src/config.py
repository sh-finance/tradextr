from logger import logger
import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, "..", ".env"), override=True)

OUTPUT_ENV = os.getenv("OUTPUT_ENV", "True") == "True"
if OUTPUT_ENV:
    logger.info(os.environ)


class Server:
    app = "main:api"
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 10000))
    reload = os.getenv("RELOAD", "False") == "True"


class OpenAI:
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    api_key = os.getenv("OPENAI_API_KEY", "sk-xxx")
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-0125")
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
