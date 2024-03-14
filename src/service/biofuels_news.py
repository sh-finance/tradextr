import os
import config
import xmltodict

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from service.spider import SpiderService
from service.mongo import mongo
from logger import logger

biofuels_news_mongo = mongo["tradextr"]["biofuels_news"]


class BiofuelsNewsService:
    @staticmethod
    def fetch_sitemap_urls(url: str = config.BiofuelsNews.sitemap_url) -> list[str]:
        """
        递归获取所有sitemap中的url
        """
        print(f"sitemap: {url}")
        try:
            page_content = SpiderService.fetch_static_page(url)
        except Exception as e:
            logger.error(e)
            return []
        root = xmltodict.parse(page_content)
        parent = root.get("sitemapindex") or root.get("urlset") or {}
        sitemaps = parent.get("sitemap") or parent.get("url") or []
        urls: list[str] = [
            sitemap.get("loc")
            for sitemap in sitemaps
            if len(sitemap.get("loc", "")) > 0
        ]
        sitemap_urls = [l for l in urls if l.endswith(".xml")]
        page_urls = [l for l in urls if not l.endswith(".xml")]
        for sitemap_url in sitemap_urls:
            sub_urls = BiofuelsNewsService.fetch_sitemap_urls(sitemap_url)
            page_urls.extend(sub_urls)
        return page_urls
