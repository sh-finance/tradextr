import datetime
from service.eia import Direction, EIAService, Query, Sort, Format, Frequency

query = Query(
    data=["value"],
    offset=30,
    length=10,
    sort=[Sort("period", Direction.asc)],
    facets={"msn": ["HVTCBUS"]},
    start=datetime.datetime(2010, 1, 1),
    # end=datetime.datetime(2011, 1, 1),
    # out=Format.xml,
    frequency=Frequency.monthly,
)
# url = EIAService.url("total-energy", query=query)
# print(url)
# res = EIAService.fetch_meta("/")
# print(res.json())

# res = EIAService.fetch_data("total-energy")
# print(res)

print(EIAService.calc_pagination(query=None, next_page=False))
