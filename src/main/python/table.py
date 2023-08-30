from __future__ import annotations
from dataclasses import dataclass

from main.python.schema import Schema


@dataclass
class Table:
    name: str
    schema: Schema
    relations: list[Table]


class AnonymousTable:

    def __init__(self, name: str | None, schema: Schema, relations: list[AnonymousTable]) -> None:
        self.name = name
        self.schema = schema
        self.relations = relations
    
    @classmethod
    def with_name(cls, name: str, schema: Schema, relations: list[AnonymousTable]):
        return AnonymousTable(name, schema, relations)
