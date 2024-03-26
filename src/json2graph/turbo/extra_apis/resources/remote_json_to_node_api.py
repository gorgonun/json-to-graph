from typing import Any, Callable, Coroutine
from json2graph.json_to_node import JsonToNode
from json2graph.node_feedback import NodeFeedback
from json2graph.relationship_reference import RelationshipReference
from json2graph.node import PartialNode
from json2graph.schema import Schema
from json2graph.turbo.extra_apis.resources.interfaces.json_to_node_api import JsonToNodeApi


class RemoteJsonToNodeApi(JsonToNodeApi):

    def __init__(self, json_to_node_actor_ref: JsonToNode):
        self.json_to_node_actor_ref = json_to_node_actor_ref

    async def next_table_increment(self):
        return await self.json_to_node_actor_ref.next_table_increment.remote()

    async def next_node_increment(self):
        return await self.json_to_node_actor_ref.next_node_increment.remote()

    async def create_table(self, name: str, schema: Schema, path: list[str] | None = None):
        return await self.json_to_node_actor_ref.create_table.remote(name, schema, path)

    async def migrate_data(
        self,
        json_data: dict[str, Any] | NodeFeedback,
        on_subnode: (
            Callable[[PartialNode, str, int, dict[str, Any]], RelationshipReference]
            | None
        ) = None,
    ):
        return await self.json_to_node_actor_ref.migrate_data.remote(json_data, on_subnode)

    async def migrate_dict(
        self,
        data: dict[str, Any],
        level: int,
        on_subnode: Callable[
            [PartialNode, str, int, dict[str, Any]],
            Coroutine[Any, Any, RelationshipReference],
        ],
        parent_field: str | None = None,
        previous_path: list[str] | None = None,
        processing_id: str | None = None,
    ):
        return await self.json_to_node_actor_ref.migrate_dict.remote(data, level, on_subnode, parent_field, previous_path, processing_id)
