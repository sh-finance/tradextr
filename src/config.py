from os import path, getenv, environ

from logger import logger
from dotenv import load_dotenv

BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, "..", ".env"), override=True)

if getenv("ENV_LOG") == "true":
    logger.info(environ)


class Server:
    app = "main:api"
    host = getenv("SERVER_HOST", "0.0.0.0")
    port = int(getenv("SERVER_PORT", 10000))


class OpenAI:
    base_url = getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    api_key = getenv("OPENAI_API_KEY", "sk-xxx")
    model = getenv("OPENAI_MODEL", "gpt-3.5-turbo-0125")
    embedding_model = getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


class Mongo:
    host = getenv("MONGO_HOST", "localhost")
    port = int(getenv("MONGO_PORT", 27017))
    username = getenv("MONGO_USERNAME", "")
    password = getenv("MONGO_PASSWORD", "")


class EIA:
    protocol = "https"
    host = "api.eia.gov"
    api_version = "v2"
    base_url = f"{protocol}://{host}/{api_version}/"
    api_keys = [k.strip() for k in getenv("EIA_API_KEYS", "").split(",") if k.strip()]


class EC:
    sitemap_url = "https://commission.europa.eu/sitemap.xml"
    # 按照顺序从左到右依次尝试查找selector 将找到的元素内容作为页面内容
    page_content_selector_priority = ["main", "body"]


class IATA:
    sitemap_url = "https://www.iata.org/sitemap.xml"
    # 按照顺序从左到右依次尝试查找selector 将找到的元素内容作为页面内容
    page_content_selector_priority = ["div.blog-detail-page", "main", "body"]


class BiofuelsNews:
    sitemap_url = "https://biofuels-news.com/sitemap.xml"
    page_content_selector_priority = ["article", "#main", "body"]
