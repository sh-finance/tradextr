import config

from langchain_core.documents import Document
from bs4 import BeautifulSoup
from re import search
from urllib.parse import urljoin, urlparse

from logger import logger

from service.es import es, es_vector_store
from service.spider import SpiderService


class EIAPageService:
    cached_urls: set[str]

    # 判断一个url是否已经被缓存
    def is_cached(self, url: str):
        return url in self.cached_urls

    # 获取所有metadata.url
    @staticmethod
    def get_cached_urls():
        query = {
            "_source": ["metadata.url"],
            "query": {"bool": {"must": [{"exists": {"field": "metadata.url"}}]}},
        }
        response = es.search(index=config.Elasticsearch.index_name, body=query)
        urls = [doc["_source"]["metadata"]["url"] for doc in response["hits"]["hits"]]
        return set(urls)

    def delete_url(self, url: str):
        query = {"query": {"term": {"metadata.url": url}}}
        es.delete_by_query(index=config.Elasticsearch.index_name, body=query)

    def reload_cached_urls(self):
        urls = EIAPageService.get_cached_urls()
        for url in urls.copy():
            # 动态网页不计入初始已缓存网页, 但后续访问中会计入
            for pattern in config.EIA.dynamic_url_patterns:
                if search(pattern, url):
                    urls.remove(url)
        self.cached_urls = urls

    def __init__(self):
        self.reload_cached_urls()

    # 判断url是否为子域
    def is_subdomain(self, domain: str, url: str):
        parsed_url = urlparse(url)
        # 检查是否是 http 或 https 协议
        if parsed_url.scheme not in ["http", "https"]:
            return False
        domain_parts = domain.split(".")
        url_domain_parts = parsed_url.netloc.split(".")
        return url_domain_parts[-len(domain_parts) :] == domain_parts

    def fetch_page_html(self, url: str):
        try:
            html = SpiderService.fetch_static_page(url)
            return html
        except Exception as e:
            logger.error(e)
            return ""

    def extract_page_content(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        for selector in config.EIA.page_content_selector_priority:
            ele = soup.select_one(selector)
            if ele:
                content = ele.get_text(separator="\n", strip=True)
                if content:
                    return content
        return soup.get_text(separator="\n", strip=True)

    def extract_sub_url_set(self, html: str, base_url: str):
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select("a")
        sub_urls = [link.attrs["href"] for link in links if link.has_attr("href")]
        sub_urls = [
            urljoin(base_url, sub_url)
            for sub_url in sub_urls
            if self.is_subdomain(config.EIA.root_domain, sub_url)
        ]
        return set(sub_urls)

    def store_page_content(self, url: str, html: str, content: str):
        doc = Document(
            page_content=content,
            metadata={
                "url": url,
                "html": html,
            },
        )
        # 删除旧文档
        self.delete_url(url)
        self.cached_urls.add(url)
        return es_vector_store.add_documents([doc])

    # 验证url是否可爬取
    def valid_url(self, url: str):
        invalid_strs = [
            "#",
            ".png",
            ".csv",
            ".doc",
            ".docx",
            ".ppt",
            ".xlsx",
            ".xls",
            ".pdf",
            ".pptx",
            ".xml",
            ".jpg",
            ".webp",
            ".gif",
        ]
        for s in invalid_strs:
            if s in url:
                return False
        return True

    def recursive_fetch_and_store_page(
        self, url: str = config.EIA.page_base_url, depth=0
    ):
        logger.info(f"url: {url} start")
        if depth > config.EIA.page_depth:
            logger.debug(f"depth > {config.EIA.page_depth}, skipped")
            return
        if self.is_cached(url):
            logger.info(f"url cached, skipped")
            return
        if not self.valid_url(url):
            logger.info(f"url invalid, skipped")
            return
        html = self.fetch_page_html(url)
        if not html:
            logger.error(f"failed to fetch html, skipped")
            return
        content = self.extract_page_content(html)
        if not content:
            logger.error(f"failed to extract content, skipped")
            return
        ids = self.store_page_content(url=url, html=html, content=content)
        if len(ids) == 0:
            logger.error(f"failed to store into es")
            return
        logger.info(f"stored page, id = {ids[0]}")
        sub_url_set = self.extract_sub_url_set(html, url)
        logger.info(f"sub url set: {sub_url_set}")
        for sub_url in sub_url_set:
            self.recursive_fetch_and_store_page(sub_url, depth + 1)


eia_page_service = EIAPageService()
