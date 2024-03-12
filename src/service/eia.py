from datetime import date
from enum import Enum
from typing import List

import requests
from config import EIA


class Frequency(Enum):
    monthly = "monthly"
    annual = "annual"


class Direction(Enum):
    asc = "asc"
    desc = "desc"


class Sort:
    column: str
    direction: Direction

    def __init__(self, column: str, direction: Direction):
        self.column = column
        self.direction = direction


class Format(Enum):
    json = "json"
    xml = "xml"


class Query:
    frequency: Frequency | None
    facets: dict[str, list[str]] | None
    data: list[str] | None
    sort: list[Sort] | None
    offset: int | None
    length: int | None
    start: date | None
    end: date | None
    out: Format | None

    def __init__(
        self,
        *,
        frequency: Frequency | None = None,
        facets: dict[str, list[str]] | None = None,
        data: List[str] | None = None,
        sort: List[Sort] | None = None,
        offset: int | None = None,
        length: int | None = None,
        start: date | None = None,
        end: date | None = None,
        out: Format | None = None,
    ):
        self.frequency = frequency
        self.facets = facets
        self.data = data
        self.sort = sort
        self.offset = offset
        self.length = length
        self.start = start
        self.end = end
        self.out = out


class EIAService:
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
        EIAService.__api_key_cursor += 1
        return EIA.api_keys[EIAService.__api_key_cursor % len(EIA.api_keys)]

    @staticmethod
    def url(route: str, *, data: bool = True, query: Query = Query()):
        """
        根据路由生成api_url
        route: 具体路由, 通过请求不带/data的url获取 `https://api.eia.gov/v2`
        """
        urlSegments = [EIA.base_url, route.strip("/"), data and "/data" or ""]
        queries = [f"api_key={EIAService.key()}"]
        if query.frequency:
            queries.append(f"frequency={query.frequency.value}")
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
                queries.append(f"sort[{i}][direction]={sort.direction.value}")
        if not (query.offset is None):
            queries.append(f"offset={query.offset}")
        if not (query.length is None):
            queries.append(f"length={query.length}")
        if query.start:
            queries.append(f'start={query.start.strftime("%Y-%m-%d")}')
        if query.end:
            queries.append(f'end={query.end.strftime("%Y-%m-%d")}')
        if query.out:
            queries.append(f"out={query.out.value}")
        url = "".join(urlSegments) + "?" + "&".join(queries)
        return url

    @staticmethod
    def calc_pagination(next_page: bool = False, query: Query | None = None):
        """
        计算分页信息
        """
        offset, length = 0, 5000
        if next_page:
            offset += length
        if not query:
            return offset, length
        if not query.length:
            out = query.out or Format.json
            """
            > Our request may generate more rows than we'd like to ingest in one API call.
            > EIA's API limits its data returns to the first 5,000 rows responsive to the request (300 rows if we request XML format).
            """
            if out == Format.json:
                length = 5000
            if out == Format.xml:
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
        url = EIAService.url(route=route, data=False)
        response = requests.get(url)
        return response

    @staticmethod
    def fetch_data(route: str, query: Query | None = None):
        """
        通过query请求某个路由下的数据
        """

        items: list[dict[str, str]] = []
        url = (
            query
            and EIAService.url(route=route, query=query)
            or EIAService.url(route=route)
        )
        body = requests.get(url).json()
        request = body.get("request", {})
        response = body.get("response", {})
        print(request)
        data, total = response.get("data", []), response.get("total", 0)
        print(total)
        items.extend(data)

        return items
