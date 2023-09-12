import os
from pymongo import MongoClient
from dotenv import load_dotenv
from main.python.json_to_node import JsonToNode
from main.python.neo4j_client import Neo4jClient
from main.python.schema import Schema
from neo4j import GraphDatabase

from main.python.schema_api import SchemaAPI


def main(threshold: float = 0.5):
    load_dotenv()

    rootName = os.environ["MONGODB_COLLECTION"]
    mongodb_url = os.environ["MONGODB_URL"]
    mongodb_database = os.environ["MONGODB_DATABASE"]
    mongodb_collection = os.environ["MONGODB_COLLECTION"]
    neo4j_url = os.environ["NEO4J_URL"]
    neo4j_user = os.environ["NEO4J_USER"]
    neo4j_password = os.environ["NEO4J_PASSWORD"]

    client = MongoClient(mongodb_url)
    db = client[mongodb_database]
    collection = db[mongodb_collection]
    schema_api = SchemaAPI(threshold)
    json_to_node = JsonToNode(rootName, schema_api)

    leaf_nodes, nodes = json_to_node.migrate_data(collection.find())
    # leaf_nodes, nodes = json_to_node.migrate_data([
    #     {
    #         "_id": "1",
    #         "name": "John",
    #         "age": 20,
    #         "address": {
    #             "street": "Main Street",
    #             "number": 123,
    #             "city": "New York"
    #         },
    #         "phones": [
    #             {
    #                 "type": "mobile",
    #                 "number": "123456789"
    #             },
    #             {
    #                 "type": "home",
    #                 "number": "987654321"
    #             }
    #         ]
    #     }
    # ])

    with Neo4jClient.from_url(neo4j_url, neo4j_user, neo4j_password) as neo4j_client:
        neo4j_client.write_nodes([*leaf_nodes, *nodes])


if __name__ == '__main__':
    main()
