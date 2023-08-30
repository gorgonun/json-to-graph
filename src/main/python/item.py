from __future__ import annotations
from typing import Any
from main.python.schema import Schema
from main.python.table import Table
import uuid


class Item():
    def __init__(self, reference: str, name: str, schema: Schema, relations: list[Item]) -> None:
        self.__reference = reference
        self.name = name
        self.schema = schema
        self.relations = relations

    def to_table(self) -> Table:
        return Table(self.name, self.schema, self.relations)
    
    def __hash__(self) -> int:
        return hash(self.__reference)


class ItemReference():
    def __init__(self, name: str | None, schema: Schema | None, relations: list[ItemReference]) -> None:
        self.__reference = uuid.uuid4()
        self.name = name
        self.schema = schema
        self.relations = relations

    def __hash__(self) -> int:
        return hash(self.__reference)


class ProcessingRequest():
    def __init__(self, item: ItemReference, data: dict[str, Any], level: int) -> None:
        self.item = item
        self.data = data
        self.level = level
