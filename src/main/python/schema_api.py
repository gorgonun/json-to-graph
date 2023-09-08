from typing import Iterable, Set, Tuple
from main.python.schema import Column, Schema


class SchemaAPI:
    def __init__(self, max_difference_between_schemas: float) -> None:
        self._schemas: dict[int, Schema] = {}
        self.max_difference_between_schemas = max_difference_between_schemas
        self.last_id = 0
    
    @property
    def schemas(self):
        return self._schemas
    
    def next_increment(self):
        self.last_id = self.last_id + 1
        return self.last_id

    def add_schema(self, schema: Schema):
        self._schemas[schema.id] = schema
    
    def update_schema(self, schema_id: int, columns: Iterable[str]):
        schema_columns = set(self._schemas[schema_id].column_information.keys())
        current_columns = set(columns)
        new_optional_columns = current_columns - schema_columns
        required_to_optional = schema_columns - current_columns
    
        self._schemas[schema_id].column_information.update({k: Column(k, True, False) for k in (new_optional_columns.union(required_to_optional))})
        return self._schemas[schema_id]

    def has(self, schema_id: str):
        return schema_id in self._schemas
    
    def new_incomplete_schema(self, column_information = None):
        schema = Schema(self.next_increment(), column_information or {})
        self._schemas[schema.id] = schema
        return schema
    
    def new_schema_from_columns(self, columns: Iterable[str]):
        schema = Schema(self.next_increment(), {k: Column(k, True, False) for k in columns})
        self._schemas[schema.id] = schema
        return schema
    
    def update_column_information(self, schema_id: str, column_name: str, is_relationship: bool):
        self._schemas[schema_id].column_information[column_name].is_relationship = is_relationship

    def find_schema_by_columns(self, columns: Iterable[str]) -> Schema | None:
        most_similar_schema: Tuple[int, float] | None = None

        for schema in self._schemas.values():
            columns_diff = set(schema.column_information.keys()) - set(columns)
            diff_rate = len(columns_diff) / len(list(columns))

            if (most_similar_schema is None and diff_rate <= self.max_difference_between_schemas) or (most_similar_schema is not None and diff_rate <= self.max_difference_between_schemas and diff_rate < most_similar_schema[1]):
                most_similar_schema = (schema.id, diff_rate)

        return self._schemas[most_similar_schema[0]] if most_similar_schema is not None else None
