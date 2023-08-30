from main.python.item import Item, ItemReference


class ProcessingAPI():
    def __init__(self) -> None:
        self.__pool: dict[ItemReference, Item | None] = {}
    
    def finished(self, item: ItemReference):
        return self.__pool[item] != None
