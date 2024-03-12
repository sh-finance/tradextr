import datetime
from service.eia import Direction, Frequency, Query, Sort, EIAService

query = Query(
    data=["value"],
    offset=30,
    length=10,
    sort=[Sort("period", Direction.asc)],
    facets={"msn": ["HVTCBUS"]},
    start=datetime.datetime(2010, 1, 1),
    frequency=Frequency.monthly,
)

EIAService.fetch_and_store_data("total-energy", query=query)
