import os
import config
import xmltodict

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from service.spider import SpiderService
from service.mongo import mongo
from logger import logger

ec_mongo = mongo["tradextr"]["ec"]


class ECService:
    @staticmethod
    def fetch_sitemap_urls() -> list[str]:
        try:
            page_content = SpiderService.fetch_static_page(config.EC.sitemap_url)
        except Exception as e:
            logger.error(e)
            return []
        root = xmltodict.parse(page_content)
        urls = root.get("urlset", {}).get("url", [])
        urls = [url.get("loc") for url in urls if len(url.get("loc", "")) > 0]
        return urls

    @staticmethod
    def fetch_page_content(url: str):
        try:
            html = SpiderService.fetch_static_page(url)
        except Exception as e:
            logger.error(e)
            return "", ""

        # store html
        url_obj = urlparse(url)
        path = url_obj.path.strip("/").split("/")
        sub_dirs = path[:-1]
        sub_filename = path[-1]
        if not sub_filename.endswith(".html"):
            sub_filename += ".html"
        dir_path = os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "..", "..", "ec", *sub_dirs
            )
        )
        full_path = os.path.abspath(os.path.join(dir_path, sub_filename))
        os.makedirs(dir_path, exist_ok=True)
        with open(full_path, "w") as file:
            file.write(html)
            file.write("\n")

        soup = BeautifulSoup(html, "html.parser")
        for selector in config.IATA.page_content_selector_priority:
            ele = soup.select_one(selector)
            if ele:
                return html, ele.get_text(separator="\n", strip=True)
        return html, soup.get_text(separator="\n", strip=True)

    @staticmethod
    def store_page_content(url: str, html: str, content: str):
        ec_mongo.find_one_and_update(
            filter={"url": url},
            update={"$set": {"content": content, "html": html}},
            upsert=True,
            return_document=False,
        )

    @staticmethod
    def fetch_sitemap_page_content():
        urls = ECService.fetch_sitemap_urls()
        for url in urls:
            html, page_content = ECService.fetch_page_content(url)
            if not page_content:
                continue
            yield url, html, page_content

    @staticmethod
    def fetch_and_store_sitemap_page_content():
        for url, html, page_content in ECService.fetch_sitemap_page_content():
            ECService.store_page_content(url, html, page_content)
