import requests
from requests.adapters import HTTPAdapter


requests_session = requests.Session()
requests_session.mount("http://", HTTPAdapter(max_retries=3))
requests_session.mount("https://", HTTPAdapter(max_retries=3))


class SpiderService:
    @staticmethod
    def fetch(url: str | bytes):
        return requests_session.get(url)

    @staticmethod
    def fetch_static_page(url: str | bytes):
        res = SpiderService.fetch(url)
        return res.text
