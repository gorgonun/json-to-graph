from dataclasses import dataclass


@dataclass
class RelationshipReference():
    table_name: str
    node_id: int

    def __str__(self) -> str:
        return f"__RelationshipReference({self.table_name}, {self.node_id})__"
