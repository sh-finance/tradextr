import datetime
from service.eia import Direction, EIAService, Query, Sort

query = Query(
    data=["value", "price"],
    offset=10,
    end=datetime.datetime.now(),
    length=3000,
    sort=[Sort("price", Direction.asc)],
)
query.data = ["price"]
url = EIAService.url("test/coal", data=True, query=query)
print(url)
