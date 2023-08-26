from main.python.schema import Schema


class SchemaAPI:
    def __init__(self) -> None:
        self._schemas = {}
    
    @property
    def schemas(self):
        return self._schemas

    def add_schema(self, schema: Schema):
        self._schemas[schema.table_id] = schema

    def has(self, table_id: str):
        return table_id in self._schemas
