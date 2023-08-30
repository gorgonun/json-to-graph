from main.python.item import ItemReference
from main.python.table import Table


class InsertOperation():
    def __init__(self, table: ItemReference, relations: list[ItemReference] | None) -> None:
        self.table = table
        self.relations = relations
