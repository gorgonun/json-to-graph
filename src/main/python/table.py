from __future__ import annotations
from dataclasses import dataclass

from main.python.schema import Schema


@dataclass
class Table:
    id: int
    name: str
    schema: Schema
    relations: list[Table]
    path: list[str]
