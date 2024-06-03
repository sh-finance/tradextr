from logger import logger

from service.ec import ECService
from service.eia.api import EiaAPIService
from service.iata import IATAService
from service.biofuels_news import BiofuelsNewsService
from service.openai import llm
from service.redis import redis
from service.es import es, es_vector_store
from service.mongo import mongo

from util.reformulate_as_separate_question import reformulate_as_separate_question

# 拉取所有路由下的所有数据 存储到mongo
# EiaAPIService.recursive_fetch_and_store_data()
# 拉取total-energy下的所有数据 存储到mongo
# EiaAPIService.recursive_fetch_and_store_data("total-energy")
# 拉取所有路由的meta信息 存储到本地
# EiaAPIService.recursive_fetch_and_store_meta()

# 拉取EC sitemap中的所有网页并存储html到本地 正文到mongo
# ECService.fetch_and_store_sitemap_page_content()

# 拉取IATA sitemap中的所有网页并存储html到本地 正文到mongo
# IATAService.fetch_and_store_sitemap_page_content()

# 拉取BiofuelsNewsService中的所有网页并存储html到本地 正文到mongo
# print(BiofuelsNewsService.fetch_sitemap_urls())

# logger.info(redis.info())

# logger.info(es.info())

# logger.info(mongo.server_info())
