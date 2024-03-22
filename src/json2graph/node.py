from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from json2graph.table import Table


@dataclass
class Node():
    id: int
    table: Table
    common_values: dict[str, Any] = field(default_factory=lambda: {})
    relationship_references: dict[str, Any] = field(default_factory=lambda: {})
    relations: list[Node] = field(default_factory=lambda: [])
    processing_id: str | None = None

    @property
    def values(self):
        return {**self.common_values, **self.relationship_references}


@dataclass
class PartialNode():
    id: int
    table: Table
    relations: list[Node] = field(default_factory=lambda: [])
