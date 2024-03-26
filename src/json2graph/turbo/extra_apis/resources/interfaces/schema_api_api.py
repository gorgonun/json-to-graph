import abc

from typing import Iterable
from json2graph.schema import Schema


class SchemaApiApi(abc.ABC):
    @abc.abstractmethod
    async def get_schemas(self) -> dict[int, Schema]:
        pass
    
    @abc.abstractmethod
    async def next_increment(self):
        pass

    @abc.abstractmethod
    async def add_schema(self, schema: Schema):
        pass
    
    @abc.abstractmethod
    async def update_schema(self, schema_id: int, columns: Iterable[str]):
        pass

    @abc.abstractmethod
    async def has(self, schema_id: str):
        pass
    
    @abc.abstractmethod
    async def new_incomplete_schema(self, column_information = None):
        pass
    
    @abc.abstractmethod
    async def new_schema_from_columns(self, columns: Iterable[str]):
        pass
    
    @abc.abstractmethod
    async def update_column_information(self, schema_id: int, column_name: str, is_relationship: bool):
        pass

    @abc.abstractmethod
    async def find_schema_by_columns(self, columns: Iterable[str]) -> Schema | None:
        pass
