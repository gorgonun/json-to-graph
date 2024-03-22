from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class AsyncRelationshipReference():
    processing_id: str

    def __str__(self) -> str:
        return f"__AsyncRelationshipReference({self.processing_id})__"
