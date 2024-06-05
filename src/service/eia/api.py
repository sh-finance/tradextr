import json
import os
import requests

from datetime import date
from enum import Enum
from typing import Callable, List
from service.mongo import mongo
from config import EIA
from logger import logger


class Frequency(Enum):
    monthly = "monthly"
    annual = "annual"


class Direction(Enum):
    asc = "asc"
    desc = "desc"


class Format(Enum):
    json = "json"
    xml = "xml"


class Sort:
    column: str
    direction: str

    def __init__(self, column: str, direction: str):
        self.column = column
        self.direction = direction


class Query:
    frequency: str | None
    facets: dict[str, list[str]] | None
    data: list[str] | None
    sort: list[Sort] | None
    offset: int | None
    length: int | None
    start: date | None
    end: date | None
    out: str | None

    def __init__(
        self,
        *,
        frequency: str | None = None,
        facets: dict[str, list[str]] | None = None,
        data: List[str] | None = None,
        sort: List[Sort] | None = None,
        offset: int | None = None,
        length: int | None = None,
        start: date | None = None,
        end: date | None = None,
        out: str | None = None,
    ):
        self.frequency = frequency
        self.facets = facets
        self.data = data
        self.sort = sort
        self.offset = offset or 0
        self.start = start
        self.end = end
        self.out = out or "json"
        if not length:
            if self.out == "json":
                self.length = 5000
            if self.out == "xml":
                self.length = 300
        else:
            self.length = length


class EiaAPIService:
    """
    doc: <https://www.eia.gov/opendata/documentation.php>
    """

    # api_key索引游标
    __api_key_cursor: int = -1

    @staticmethod
    def key():
        """
        获取一个api_key, 多个api_key则负载均衡
        """
        EiaAPIService.__api_key_cursor += 1
        return EIA.api_keys[EiaAPIService.__api_key_cursor % len(EIA.api_keys)]

    @staticmethod
    def url(route: str, *, data: bool = True, query: Query | None = None):
        """
        根据路由生成api_url
        route: 具体路由, 通过请求不带/data的url获取 `https://api.eia.gov/v2`
        """
        query = query or Query()
        urlSegments = [
            EIA.api_base_url,
            route.strip(os.path.sep),
            data and "/data" or "",
        ]
        queries = [f"api_key={EiaAPIService.key()}"]
        if query.frequency:
            queries.append(f"frequency={query.frequency}")
        if query.facets:
            for facet in query.facets:
                values = query.facets[facet]
                for v in values:
                    queries.append(f"facets[{facet}][]={v}")
        if query.data:
            for d in query.data:
                queries.append(f"data[]={d}")
        if query.sort:
            for i, sort in enumerate(query.sort):
                queries.append(f"sort[{i}][column]={sort.column}")
                queries.append(f"sort[{i}][direction]={sort.direction}")
        if not (query.offset is None):
            queries.append(f"offset={query.offset}")
        if not (query.length is None):
            queries.append(f"length={query.length}")
        if query.start:
            queries.append(f'start={query.start.strftime("%Y-%m-%d")}')
        if query.end:
            queries.append(f'end={query.end.strftime("%Y-%m-%d")}')
        if query.out:
            queries.append(f"out={query.out}")
        url = "".join(urlSegments) + "?" + "&".join(queries)
        return url

    @staticmethod
    def calc_pagination(*, next_page: bool = False, query: Query | None = None):
        """
        计算分页信息
        """
        offset, length = 0, 5000
        if next_page:
            offset += length
        if not query:
            return offset, length
        if not query.length:
            out = query.out or "json"
            """
            > Our request may generate more rows than we'd like to ingest in one API call.
            > EIA's API limits its data returns to the first 5,000 rows responsive to the request (300 rows if we request XML format).
            """
            if out == "json":
                length = 5000
            if out == "xml":
                length = 300
        else:
            length = query.length
        if query.offset:
            if next_page:
                offset = query.offset + length
            else:
                offset = query.offset
        else:
            if next_page:
                offset = length
            else:
                offset = 0
        return offset, length

    @staticmethod
    def fetch_meta(route: str):
        """
        获取某个路由的meta信息
        """
        url = EiaAPIService.url(route=route, data=False)
        response = requests.get(url)
        body = response.json()
        response = body.get("response", {})
        return response

    @staticmethod
    def fetch_data(
        route: str,
        *,
        query: Query | None = None,
        handler: Callable[[list[dict[str, str]], str], None],
    ) -> None:
        """
        通过query请求某个路由下的数据
        """
        query = query or Query()
        data = []
        total = 0
        while True:
            url = EiaAPIService.url(route=route, query=query)
            logger.info(f"url={url}")
            try:
                body = requests.get(url).json()
                response = body.get("response", {})
                data, total = response.get("data", []), response.get("total", 0)
                handler(data, route)
            except Exception as e:
                """
                api有接口频率限制 请求频率太高可能会失败 碰到异常直接跳过这一部分
                Todo: 支持查找&补全缺失部分
                """
                print(e)
                logger.error(e)
            finally:
                # 继续获取下一页
                offset, _length = EiaAPIService.calc_pagination(
                    next_page=True, query=query
                )
                logger.info(f"next_page_offset: {offset}, total: {total}")
                if offset >= int(total):
                    return
                query.offset = offset

    @staticmethod
    def store_data(data: list[dict[str, str]], route: str):
        tradextr = mongo["tradextr"]
        eia = tradextr["eia"]
        eia.insert_many(data)

    @staticmethod
    def fetch_and_store_data(route: str, *, query: Query | None = None):
        EiaAPIService.fetch_data(
            route=route, query=query, handler=EiaAPIService.store_data
        )

    @staticmethod
    def recursive_fetch_and_store_data(route: str = ""):
        meta = EiaAPIService.fetch_meta(route)
        logger.info(route)
        routes = meta.get("routes", [])
        if routes:
            for sub_route in routes:
                sub_route_id = sub_route.get("id", "")
                if not sub_route_id:
                    logger.warning(f"sub_route_id is empty: {sub_route_id}")
                    continue
                EiaAPIService.recursive_fetch_and_store_data(
                    os.path.sep.join([route, sub_route_id])
                )
        else:
            data = meta.get("data", {})
            data_keys = data.keys()
            for frequency in meta.get("frequency", []):
                frequency_id = frequency.get("id", "")
                query = Query(frequency=frequency_id, data=data_keys)
                EiaAPIService.fetch_and_store_data(route=route, query=query)

    @staticmethod
    def recursive_fetch_and_store_meta(route: str = ""):
        meta = EiaAPIService.fetch_meta(route)
        logger.info(route)
        # meta写入到本地
        sub_path = route.strip(os.path.sep) or "index"
        sub_dir = sub_path.split(os.path.sep)[:-1]
        sub_filename = sub_path.split(os.path.sep)[-1]
        dir_path = os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "meta",
                *sub_dir,
            )
        )
        full_path = os.path.abspath(os.path.join(dir_path, f"{sub_filename}.json"))
        os.makedirs(dir_path, exist_ok=True)
        with open(full_path, "w") as file:
            file.write(json.dumps(meta, indent=2))
            file.write("\n")

        routes = meta.get("routes", [])
        if routes:
            for sub_route in routes:
                sub_route_id = sub_route.get("id", "")
                if not sub_route_id:
                    logger.warning(f"sub_route_id is empty: {sub_route_id}")
                    continue
                EiaAPIService.recursive_fetch_and_store_meta(
                    os.path.sep.join([route, sub_route_id])
                )
