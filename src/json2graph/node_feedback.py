from dataclasses import dataclass

from json2graph.async_relationship_reference import AsyncRelationshipReference


@dataclass
class NodeFeedback:
    data: dict
    level: int
    processing_id: AsyncRelationshipReference
    parent_field: str
