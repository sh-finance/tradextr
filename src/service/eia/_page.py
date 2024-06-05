import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from urllib.robotparser import RobotFileParser
from collections import deque
from langchain_openai import OpenAIEmbeddings
from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_core.documents.base import Document
from datetime import datetime, timezone, timedelta

import config

# use log to find errors while running
from logger import logger

from service.openai import llm, embedding
from service.es import es, es_vector_store

"""
copy from: ES_Database_setup/Upload_eia_to_es.py
"""

# User-Agent header for the requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


# test if the url scraped from eia already stored or not
def document_exists(url):
    query = {"query": {"term": {"metadata.url": url}}}
    response = es.search(body=query)
    return response["hits"]["total"]["value"] > 0


# 获取所有metadata.url
def get_cached_url():
    query = {
        "_source": ["metadata.url"],
        "query": {"bool": {"must": [{"exists": {"field": "metadata.url"}}]}},
    }
    response = es.search(body=query)
    return [doc["_source"]["metadata"]["url"] for doc in response["hits"]["hits"]]


# 已访问过的网页
visited = set(get_cached_url())


# 建立函数方便爬取不同网页
def store_es(url, headers=headers):
    # url 为对应网页
    # 返回页面源代码
    response = requests.get(url=url, headers=headers)
    html_text = response.text
    # 用soup筛选<p>获取文本
    soup = BeautifulSoup(html_text, "html.parser")
    ele = soup.select("p")
    # 用full_text来存储页面文本信息
    full_text = ""
    # 遍历response set去除<xxx> 保留文本
    # 网页爬取ele[27:-2], 之前的都是一样的menu curel oil....etc. 去除重复部分方便搜索
    for element in ele[27:-2]:
        full_text = full_text + element.get_text(separator="\n", strip=True)
    # 获取标题
    try:
        ele_title = soup.select("title")
        element = ele_title[0]
        title = element.get_text(separator="\n", strip=True)
    except:
        title = full_text[:40] + "..."
    # 获取时间
    try:
        # most websites should be able to get, some press in iata domain cannot, use soup to select
        ele_date = soup.find_all("span", class_="date")
        date_string = ele_date[0].get_text()
        # should be look like April 23, 2022
        # convert into same format
        date = datetime.strptime(date_string, "%B %d, %Y")
        # 存入日期字符串
        date_str = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    except:
        # 赋予空
        date_str = ""
    # 尝试添加检索关键词
    # keyword有[biofuel,biodiesel,rins ，lcfs ，uco，carbon intensity score]
    # 查询文本full_text里面有没有这些词
    key_type = ""
    if re.search("biofuel", full_text, re.IGNORECASE) or re.search(
        "biofuel", title, re.IGNORECASE
    ):
        key_type = key_type + "biofuel,"
    if re.search("biodiesel", full_text, re.IGNORECASE) or re.search(
        "biodiesel", title, re.IGNORECASE
    ):
        key_type = key_type + "biodiesel,"
    # LCFS
    if re.search("low carbon fuel", full_text, re.IGNORECASE) or re.search(
        "low carbon fuel", title, re.IGNORECASE
    ):
        key_type = key_type + "low carbon fuel,LCFS"
    # RFS
    if re.search("renewable fuel", full_text, re.IGNORECASE) or re.search(
        "renewable fuel", title, re.IGNORECASE
    ):
        key_type = key_type + "renewable fuel,RFS,"
    # RINS
    if re.search(
        "renewable identification number", full_text, re.IGNORECASE
    ) or re.search("renewable identification number", title, re.IGNORECASE):
        key_type = key_type + "renewable identification number, RINS,"
    # used cooking oil, UCO
    if re.search("used cooking oil", full_text, re.IGNORECASE) or re.search(
        "used cooking oil", title, re.IGNORECASE
    ):
        key_type = key_type + "used cooking oil,UCO"
    # carbon intensity score,
    if re.search("carbon intensity", full_text, re.IGNORECASE) or re.search(
        "carbon intensity", title, re.IGNORECASE
    ):
        key_type = key_type + "carbon intensity,"
    # 将该得到的数据text,html,url导入es,并用openai embedding向量化
    es_vector_store.add_documents(
        documents=[
            Document(
                page_content=full_text,
                metadata={
                    "url": url,
                    "html": html_text,
                    "title": title,
                    "date": date_str,
                    "type": key_type,
                },
            )
        ]
    )


# Initialize the RobotFileParser
rp = RobotFileParser()


# Function to check if fetching a URL is allowed
def can_fetch(url):
    rp.set_url(requests.compat.urljoin(url, "/robots.txt"))  # type: ignore
    rp.read()
    return rp.can_fetch(headers["User-Agent"], url)


# Function to extract links from the given URL
def get_links(url, domain):
    if can_fetch(url):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if response.encoding is None:
                response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                full_link = requests.compat.urljoin(url, link["href"])  # type: ignore
                if full_link.startswith(domain):
                    yield full_link
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    else:
        print(f"Access denied by robots.txt: {url}")


# Function to crawl the web starting from a base URL
def crawl(start_url):
    domain = "{uri.scheme}://{uri.netloc}".format(uri=requests.utils.urlparse(start_url))  # type: ignore
    queue = deque([start_url])

    while queue:
        url = queue.popleft()
        if url not in visited:
            # 这里的url都是没有爬过的
            # 把这里的url爬取一下获取文本内容，使用try
            visited.add(url)
            # 做判断，此处输出的url都是未入库的，直接用这些url做爬取传输
            if not document_exists(url):
                # print(f"Visiting: {url}")
                # url里面有些是下载链接 （xlsx）和重复网页 （#）不需要重复爬取
                if "#" not in url and not url.endswith(
                    (".xls", ".xlsx", ".mp3", ".csv", ".zip")
                ):
                    try:
                        # sleep for a while
                        sleep(2)
                        store_es(url)
                    except Exception as e:
                        print(e.with_traceback())  # type: ignore
                        logger.error(e)
                else:
                    print("Invalid url: " + url)
            else:
                print("Repeated url: " + url)
            # now use loop to get the next url
            try:
                for next_url in get_links(url, domain):
                    if next_url not in visited:
                        queue.append(next_url)
            except Exception as e:
                print(e.with_traceback())  # type: ignore
                logger.error(e)


# Start the crawler


# Set the domain and start URL
domain = "https://www.eia.gov"
start_url = domain
# Start crawling from the base URL


class EiaPageService:
    @staticmethod
    def start_crawl():
        crawl(config.EIA.page_base_url)
