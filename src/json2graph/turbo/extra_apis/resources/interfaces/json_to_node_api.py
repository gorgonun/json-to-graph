import abc
from typing import Any, Callable, Coroutine
from json2graph.node_feedback import NodeFeedback
from json2graph.relationship_reference import RelationshipReference
from json2graph.node import PartialNode
from json2graph.schema import Schema


class JsonToNodeApi(abc.ABC):

    @abc.abstractmethod
    async def next_table_increment(self):
        pass

    @abc.abstractmethod
    async def next_node_increment(self):
        pass

    @abc.abstractmethod
    async def create_table(self, name: str, schema: Schema, path: list[str] | None = None):
        pass

    @abc.abstractmethod
    async def migrate_data(
        self,
        json_data: dict[str, Any] | NodeFeedback,
        on_subnode: (
            Callable[[PartialNode, str, int, dict[str, Any]], RelationshipReference]
            | None
        ) = None,
    ):
        pass

    @abc.abstractmethod
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
        pass
