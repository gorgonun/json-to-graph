from typing import Iterable, Set, Tuple
from main.python.schema import Schema


class SchemaAPI:
    def __init__(self, max_difference_between_schemas: int) -> None:
        self._schemas: dict[str, Schema] = {}
        self.max_difference_between_schemas = max_difference_between_schemas
    
    @property
    def schemas(self):
        return self._schemas

    def add_schema(self, schema: Schema):
        self._schemas[schema.table_id] = schema
    
    def update_schema(self, name: str, columns: Iterable[str]):
        schema_columns = set(self._schemas[name].column_information.keys())
        current_columns = set(columns)
        new_optional_columns = current_columns - schema_columns
        required_to_optional = schema_columns - current_columns
    
        self._schemas[name].column_information.update({k: False for k in (new_optional_columns + required_to_optional)})
        return self._schemas[name]

    def has(self, table_id: str):
        return table_id in self._schemas
    
    def new_incomplete_schema(self, table_id: str, **kwargs):
        schema = Schema(table_id, **kwargs)
        self._schemas[table_id] = schema
        return schema
    
    def new_schema_from_columns(self, table_id: str, columns: Iterable[str]):
        schema = Schema(table_id, {k: None for k in columns}, set(), 0)
        self._schemas[table_id] = schema
        return schema

    def find_schema_by_columns(self, columns: Iterable[str], default: Schema) -> Schema:
        most_similar_schema: Tuple[str, int] | None = None

        for schema in self._schemas.values():
            columns_diff = set(schema.column_information.keys()) - set(columns)
            diff_rate = len(columns_diff) / len(columns)

            if (most_similar_schema is None and diff_rate <= self.max_difference_between_schemas) or (diff_rate <= self.max_difference_between_schemas and diff_rate < most_similar_schema[1]):
                most_similar_schema = (schema.table_id, diff_rate)

        return self._schemas[most_similar_schema[1]] if most_similar_schema is not None else default

    @classmethod
    def new_schema_from_columns(cls, table_id: str, columns: Iterable[str]):
        return Schema(table_id, {k: None for k in columns}, set(), 0)

    @classmethod
    def new_anonimous_schema(cls, **kwargs):
        return Schema("", **kwargs)
