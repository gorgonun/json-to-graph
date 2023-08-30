from __future__ import annotations
from dataclasses import dataclass, field

from main.python.table import Table


@dataclass
class Node():
    name: str
    table: Table
    relations: list[Node] = field(default_factory=lambda: [])
