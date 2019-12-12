#https://realpython.com/data-engineer-interview-questions-python/

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Note: This database is not created until it is populated by some data
db = client["example_database"]

customers = db["customers"]
items = db["items"]

customers_data = [{ "firstname": "Bob", "lastname": "Adams" },
                  { "firstname": "Amy", "lastname": "Smith" },
                  { "firstname": "Rob", "lastname": "Bennet" },]
items_data = [{ "title": "USB", "price": 10.2 },
              { "title": "Mouse", "price": 12.23 },
              { "title": "Monitor", "price": 199.99 },]

customers.insert_many(customers_data)
items.insert_many(items_data)

# Just add "boughtitems" to the customer where the firstname is Bob
bob = customers.update_many(
        {"firstname": "Bob"},
        {
            "$set": {
                "boughtitems": [
                    {
                        "title": "USB",
                        "price": 10.2,
                        "currency": "EUR",
                        "notes": "Customer wants it delivered via FedEx",
                        "original_item_id": 1
                    }
                ]
            },
        }
    )

amy = customers.update_many(
        {"firstname": "Amy"},
        {
            "$set": {
                "boughtitems":[
                    {
                        "title": "Monitor",
                        "price": 199.99,
                        "original_item_id": 3,
                        "discounted": False
                    }
                ]
            } ,
        }
    )
print(type(amy))  # pymongo.results.UpdateResult
customers.create_index([("name", pymongo.DESCENDING)])
items = customers.find().sort("name", pymongo.ASCENDING)

for item in items:
     print(item.get('boughtitems'))




#LIST OF UNIQUE NAMES
print(customers.distinct("firstname"))

for i in customers.find({"$or": [{'firstname':'Bob'}, {'firstname':'Amy'}]},
                                  {'firstname':1, 'boughtitems':1, '_id':0}):
     print(i)