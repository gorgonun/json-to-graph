import os
from pymongo import MongoClient
from dotenv import load_dotenv
from main.python.schema import Schema

from main.python.schema_api import SchemaAPI


def main(threshold: float = 0.5):
    load_dotenv()
    client = MongoClient(os.environ["MONGODB_URL"])
    db = client["test"]
    collection = db[os.environ["MONGODB_COLLECTION"]]
    schema_api = SchemaAPI()
    rootName = os.environ("MONGODB_COLLECTION")

    for doc in collection.find():
        if schema_api.has(rootName):
            schema_api.update_schema(rootName, doc.keys())
        else:
            schema_api.add_schema(Schema(rootName, {k: True for k in doc.keys()}, set(), 0))

        for (k, v) in doc.items():
            if isinstance(v, dict):
                if schema_api.has(k):
                    schema_api.update_schema(k, v.keys())
                else:
                    schema_api.add_schema(Schema(k, {k: True for k in v.keys()}, set(), 0))
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        if schema_api.has(k):
                            schema_api.update_schema(k, item.keys())
                        else:
                            schema_api.add_schema(Schema(k, {k: True for k in item.keys()}, set(), 0))


if __name__ == '__main__':
    main()
