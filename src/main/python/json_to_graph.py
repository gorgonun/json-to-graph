from collections import deque
from typing import Any, Iterable
from main.python.item import ItemReference, ProcessingRequest
from main.python.node import Node
from main.python.processing_api import ProcessingAPI
from main.python.schema import Schema

from main.python.schema_api import SchemaAPI
from main.python.table import AnonymousTable, Table


class JsonToGraph():
    def __init__(self, root_name: str, schema_api: SchemaAPI) -> None:
        self.root_name = root_name
        self.schema_api = schema_api
        self.root_table = Table(root_name, schema_api.new_incomplete_schema(root_name))
        self.processing_queue = deque()
        self.processing_api = ProcessingAPI()
        self.table_mapping: dict[str, Table] = {}

    def create_table(self, name: str, schema: Schema):
        table = Table(name, schema)
        self.table_mapping[schema.table_id] = table
        return table

    def migrate_data(self, json_data: Iterable[dict[str, Any] | list[Any]]):
        for doc in json_data:
            node = self.migrate_dict(doc)
        
    def migrate_dict(self, data: dict[str, Any], level: int, parent_field: str | None = None):
        node = None

        if level == 0:
            schema = self.schema_api.update_schema(self.root_name, data.keys())
            table = self.table_mapping.get(self.root_name, self.create_table(self.root_name, schema))
            node = Node(data["_id"], table)
        
        elif level > 0 and parent_field:
            schema = self.schema_api.find_schema_by_columns(data.keys(), self.schema_api.new_schema_from_columns(parent_field, data.keys()))
            table = self.table_mapping.get(parent_field, self.create_table(parent_field, schema))
            node = Node(parent_field, table)

        else:
            raise RuntimeError("Invalid level or parent")
            
        for (k, v) in data.items():
            if isinstance(v, dict):
                node.relations.append(self.migrate_dict(v, level + 1, k))
            elif isinstance(v, list):
                node.relations.extend([self.migrate_dict(x, level + 1, k) for x in v])

        return node
    
    # def request_processing(self, data: dict[str, Any] | Iterable[dict[str, Any]], level: int):
    #     item_reference = ItemReference()
    #     self.processing_queue.append(ProcessingRequest(item_reference, data, level))
    #     return item_reference
