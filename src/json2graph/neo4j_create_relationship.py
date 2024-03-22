from dataclasses import dataclass


@dataclass
class Neo4JCreateRelationship():
    origin_id: int
    destination_id: int
    relationship_name: str
