from dataclasses import dataclass


@dataclass
class Neo4JRelationshipData():
    origin_id: int
    origin_label: str
    destination_id: int
    destination_label: str
    relationship_name: str
