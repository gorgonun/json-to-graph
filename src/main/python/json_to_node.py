from typing import Any, Iterable
from main.python.relationship_reference import RelationshipReference
from main.python.node import Node, PartialNode
from main.python.schema import Schema
from main.python.schema_api import SchemaAPI
from main.python.table import Table


class JsonToNode():
    def __init__(self, root_name: str, schema_api: SchemaAPI) -> None:
        self.root_name = root_name
        self.schema_api = schema_api
        self.table_mapping: dict[str, Table] = {}
        self.incremental_ids: dict[str, int] = {
            "table": 0,
            "node": 0
        }
        self.root_table = self.create_table(root_name, schema_api.new_incomplete_schema())

    def next_table_increment(self):
        self.incremental_ids["table"] = self.incremental_ids["table"] + 1
        return self.incremental_ids["table"]
    
    def next_node_increment(self):
        self.incremental_ids["node"] = self.incremental_ids["node"] + 1
        return self.incremental_ids["node"]

    def create_table(self, name: str, schema: Schema, path: list[str] | None = None):
        table = Table(self.next_table_increment(), name, schema, [], path or [])
        self.table_mapping[name] = table
        return table

    def migrate_data(self, json_data: Iterable[dict[str, Any]]):
        result: list[Node] = []
        result_leaft_nodes: list[Node] = []

        for doc in json_data:
            leaft_nodes, node = self.migrate_dict(doc, 0)
            result.append(node)
            result_leaft_nodes.extend(leaft_nodes)
        
        return result_leaft_nodes, result
        
    def migrate_dict(self, data: dict[str, Any], level: int, parent_field: str | None = None, previous_path: list[str] | None = None):
        node = None
        values = {
            "common": {},
            "relationship": {}
        }
        leaf_nodes = []

        if level == 0:
            schema = self.schema_api.update_schema(self.root_table.schema.id, data.keys())
            node = PartialNode(id=self.next_node_increment(), table=self.root_table, relations=[])
        
        elif level > 0 and parent_field:
            schema = self.schema_api.find_schema_by_columns(data.keys())
            table = self.table_mapping.get(parent_field)

            if schema:
                self.schema_api.update_schema(schema.id, data.keys())

            if not schema and not table:
                schema = self.schema_api.new_schema_from_columns(data.keys())
                table = self.create_table(parent_field, schema, previous_path)
            
            elif schema and not table:
                table = self.create_table(parent_field, schema, previous_path)

            node = PartialNode(id=self.next_node_increment(), table=table, relations=[])

        else:
            raise RuntimeError(f"Invalid level {level} or parent {parent_field}")
            
        for (k, v) in data.items():
            if not v:
                continue
            if isinstance(v, dict):
                new_leaf_nodes, relation = self.migrate_dict(v, level + 1, k)
                node.relations.append(relation)
                values["relationship"][k] = RelationshipReference(relation.table.name, relation.id)
                self.schema_api.update_column_information(node.table.schema.id, k, True)
                leaf_nodes.extend([*new_leaf_nodes, relation])
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        new_leaf_nodes, relation = self.migrate_dict(item, level + 1, k)
                        node.relations.append(relation)
                        values["relationship"][k] = RelationshipReference(relation.table.name, relation.id)
                        self.schema_api.update_column_information(node.table.schema.id, k, True)
                        leaf_nodes.extend([*new_leaf_nodes, relation])
                    else:
                        values["common"][k] = v
            else:
                values["common"][k] = v

        return (leaf_nodes, Node(id=node.id, table=node.table, common_values=values["common"], relationship_references=values["relationship"], relations=node.relations))
    
    def link_table(self, src: Table, dst: Table):
        src.relations[dst.id] = dst
