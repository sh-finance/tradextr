import config

from urllib.parse import quote_plus
from pymongo import MongoClient

mongo = MongoClient(
    f"mongodb://{quote_plus(config.Mongo.username)}:{quote_plus(config.Mongo.password)}@{config.Mongo.host}:{config.Mongo.port}",
    document_class=dict[str, str],
)
