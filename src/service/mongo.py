import config

from urllib.parse import quote_plus
from pymongo import MongoClient

mongo = MongoClient(
    f"mongodb://{quote_plus(config.Mongo.username)}:{quote_plus(config.Mongo.password)}@{config.Mongo.host}:{config.Mongo.port}",
    document_class=dict[str, str],
)

# print(mongo.list_database_names())
tradextr = mongo["tradextr"]
collection_names = tradextr.list_collection_names()
# eia = tradextr["eia"]
collection_name = "eia"
if not (collection_name in collection_names):
    tradextr.create_collection(collection_name)
    print(f"collection `{collection_name}` created.")
