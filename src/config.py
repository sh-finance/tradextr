from os import environ, path, getenv
from urllib.parse import quote_plus
from re import compile
from dotenv import load_dotenv
from logging import getLevelName


BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, "..", ".env"), override=True)


class Logger:
    level = getLevelName(getenv("LOGGER_LEVEL", "INFO"))


class Server:
    app = "main:api"
    host = getenv("SERVER_HOST", "0.0.0.0")
    port = int(getenv("SERVER_PORT", 10000))
    reload = getenv("SERVER_RELOAD") == "true"
    reload_includes = ["*.py", "*.json"]
    reload_excludes = ["*.log", "*.tmp"]
    reload_delay = 1


class OpenAI:
    base_url = getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    api_key = getenv("OPENAI_API_KEY", "sk-xxx")
    model = getenv("OPENAI_MODEL", "gpt-3.5-turbo-0125")
    embedding_model = getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


class Tavily:
    __api_key_cursor = 0

    api_keys = [
        key.strip()
        for key in getenv("TAVILY_API_KEYS", "").split(sep=",")
        if len(key) > 0
    ]
    max_results = int(getenv("TAVILY_MAX_RESULTS", 5))

    @staticmethod
    def api_key():
        key = Tavily.api_keys[Tavily.__api_key_cursor % len(Tavily.api_keys)]
        Tavily.__api_key_cursor += 1
        return key


# LangChain中使用Tavily只能通过环境变量的方式注入key
# 默认使用第一个key
environ["TAVILY_API_KEY"] = Tavily.api_keys[0]


class Mongo:
    host = getenv("MONGO_HOST", "localhost")
    port = int(getenv("MONGO_PORT", 27017))
    username = getenv("MONGO_USERNAME", "")
    password = getenv("MONGO_PASSWORD", "")


class Redis:
    host = getenv("REDIS_HOST", "localhost")
    port = int(getenv("REDIS_PORT", 6379))
    username = getenv("REDIS_USERNAME", "")
    password = getenv("REDIS_PASSWORD", "")
    url = (
        getenv("REDIS_URL", "")
        or f"redis://{quote_plus(username)}:{quote_plus(password)}@{host}:{port}"
    )


class Elasticsearch:
    index_name = getenv("ES_INDEX_NAME", "unknown")
    url = getenv("ES_URL", "http://localhost:9200")


class EIA:
    root_domain = "eia.gov"
    protocol = "https"
    host = "api.eia.gov"
    api_version = "v2"
    api_base_url = f"{protocol}://{host}/{api_version}/"
    api_keys = [k.strip() for k in getenv("EIA_API_KEYS", "").split(",") if k.strip()]
    page_base_url = "https://www.eia.gov/"
    # 匹配规则的地址每次抓取都需要更新
    dynamic_url_patterns = [
        # 所有以`/`结尾的地址
        compile(r"/$")
    ]
    # 按照顺序从左到右依次尝试查找selector 将找到的元素内容作为页面内容
    page_content_selector_priority = [".article", ".pagecontent", "body"]
    # 按照顺序从左到右依次尝试查找selector 将找到的元素内容作为页面内容
    page_date_selector_priority = [".date"]
    # 爬取的网页最大深度, 首页深度视为0
    page_depth = 128


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
