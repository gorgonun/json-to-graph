from typing import Any, Callable, Coroutine
from json2graph.id_manager_api import IdManagerApi
from json2graph.node_feedback import NodeFeedback
from json2graph.relationship_reference import RelationshipReference
from json2graph.node import Node, PartialNode
from json2graph.schema import Schema
from json2graph.table import Table
from json2graph.turbo.extra_apis.resources.remote_schema_api_api import RemoteSchemaApiApi


class JsonToNode():
    def __init__(self, root_name: str, schema_api: RemoteSchemaApiApi, id_manager: IdManagerApi) -> None:
        self.root_name = root_name
        self.schema_api = schema_api
        self.table_mapping: dict[str, Table] = {}
        self.id_manager = id_manager
        self.root_table = None

    async def create_root_table(self):
        return await self.create_table(self.root_name, await self.schema_api.new_incomplete_schema())

    async def next_table_increment(self):
        result = await self.id_manager.get_id_increment(f"{self.root_name}_table", create=True)
        if not result:
            raise RuntimeError("Table increment could not be created")
        
        return result
    
    async def next_node_increment(self):
        result = await self.id_manager.get_id_increment(f"{self.root_name}_node", create=True)
        if not result:
            raise RuntimeError("Node increment could not be created")
        
        return result

    async def create_table(self, name: str, schema: Schema, path: list[str] | None = None):
        table = Table(await self.next_table_increment(), name, schema, [], path or [])
        self.table_mapping[name] = table
        return table
    
    async def on_subnode_default(self, node: PartialNode, src_column: str, level: int, sub_node: dict[str, Any]):
        relation = await self.migrate_dict(sub_node, level + 1, src_column, self.on_subnode_default)
        node.relations.append(relation)
        return RelationshipReference(relation.table.name, relation.id)

    async def migrate_data(self, json_data: dict[str, Any] | NodeFeedback, on_subnode: Callable[[PartialNode, str, int, dict[str, Any]], RelationshipReference] | None = None):
        if isinstance(json_data, NodeFeedback):
            return await self.migrate_dict(json_data.data, json_data.level, on_subnode or self.on_subnode_default, parent_field=json_data.parent_field, processing_id=str(json_data.processing_id))
        return await self.migrate_dict(json_data, 0, on_subnode=on_subnode or self.on_subnode_default)
        
    async def migrate_dict(self, data: dict[str, Any], level: int, on_subnode: Callable[[PartialNode, str, int, dict[str, Any]], Coroutine[Any, Any, RelationshipReference]], parent_field: str | None = None, previous_path: list[str] | None = None, processing_id: str | None = None):
        node = None
        values = {
            "common": {},
            "relationship": {},
            "processing_id": processing_id
        }

        if level == 0:
            if not self.root_table:
                self.root_table = await self.create_root_table()

            schema = await self.schema_api.update_schema(self.root_table.schema.id, data.keys())
            self.root_table.schema = schema
            node = PartialNode(id=await self.next_node_increment(), table=self.root_table, relations=[])
        
        elif level > 0 and parent_field:
            schema = await self.schema_api.find_schema_by_columns(data.keys())
            table = self.table_mapping.get(parent_field)

            if schema:
                await self.schema_api.update_schema(schema.id, data.keys())

            if not schema and not table:
                schema = await self.schema_api.new_schema_from_columns(data.keys())
                table = await self.create_table(parent_field, schema, previous_path)
            
            elif schema and not table:
                table = await self.create_table(parent_field, schema, previous_path)

            node = PartialNode(id=await self.next_node_increment(), table=table, relations=[])

        else:
            raise RuntimeError(f"Invalid level {level} or parent {parent_field}")
            
        for (k, v) in data.items():
            if not v:
                continue
            if isinstance(v, dict):
                reference = await on_subnode(node, k, level, v)
                values["relationship"][k] = reference
                await self.schema_api.update_column_information(node.table.schema.id, k, True)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        reference = await on_subnode(node, k, level, item)
                        values["relationship"][k] = reference
                        await self.schema_api.update_column_information(node.table.schema.id, k, True)
                    else:
                        values["common"][k] = v
            else:
                values["common"][k] = v

        return Node(id=node.id, table=node.table, common_values=values["common"], relationship_references=values["relationship"], relations=node.relations, processing_id=values["processing_id"])
