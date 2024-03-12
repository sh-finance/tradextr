from service.mongo import mongo

print(mongo.list_database_names())
tradextr = mongo["tradextr"]
print(tradextr.list_collection_names())
eia = tradextr["eia"]
for index in eia.list_indexes():
    print(index)
