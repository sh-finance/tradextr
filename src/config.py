import os

from logger import logger
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


class EIA:
    protocol = "https"
    host = "api.eia.gov"
    api_version = "v2"
    base_url = f"{protocol}://{host}/{api_version}"
    api_keys = [
        k.strip() for k in os.getenv("EIA_API_KEYS", "").split(",") if k.strip()
    ]
