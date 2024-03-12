import datetime
from service.eia import Direction, EIAService, Query, Sort, Format, Frequency
from logger import logger

query = Query(
    data=["value"],
    sort=[Sort("period", Direction.asc)],
    facets={"msn": ["HVTCBUS"]},
    start=datetime.datetime(2020, 1, 1),
    # end=datetime.datetime(2011, 1, 1),
    # out=Format.xml,
    frequency=Frequency.monthly,
)


def handler(data: list[dict[str, str]]):
    logger.info(data)


EIAService.fetch_data(route="total-energy", query=query, handler=handler)
