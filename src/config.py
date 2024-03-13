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


class Mongo:
    host = os.getenv("MONGO_HOST", "localhost")
    port = int(os.getenv("MONGO_PORT", 27017))
    username = os.getenv("MONGO_USERNAME", "")
    password = os.getenv("MONGO_PASSWORD", "")


class EIA:
    protocol = "https"
    host = "api.eia.gov"
    api_version = "v2"
    base_url = f"{protocol}://{host}/{api_version}/"
    api_keys = [
        k.strip() for k in os.getenv("EIA_API_KEYS", "").split(",") if k.strip()
    ]


class EC:
    sitemap_url = "https://commission.europa.eu/sitemap.xml"
    # 按照顺序从左到右依次尝试查找selector 将找到的元素内容作为页面内容
    page_content_selector_priority = ["main", "body"]


class IATA:
    sitemap_url = "https://www.iata.org/sitemap.xml"
    # 按照顺序从左到右依次尝试查找selector 将找到的元素内容作为页面内容
    page_content_selector_priority = ["div.blog-detail-page", "main", "body"]
