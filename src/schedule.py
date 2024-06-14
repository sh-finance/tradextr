from sched import scheduler
from time import time, sleep
from threading import Thread

from service.eia.page import eia_page_service

from logger import logger

scheduler = scheduler(time, sleep)


def eia_page():
    try:
        eia_page_service.recursive_fetch_and_store_page()
    except Exception as e:
        logger.error(e)
    finally:
        eia_page_service.reload_cached_url_set()
        # 每天一次
        scheduler.enter(60 * 60 * 24, 1, eia_page)


scheduler.enter(0, 1, eia_page)


def scheduler_run():
    thread = Thread(target=scheduler.run)
    thread.start()
