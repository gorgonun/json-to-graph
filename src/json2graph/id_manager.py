class IdManager():
    def __init__(self, meta: dict[str, str] | None) -> None:
        self.__ids = {}
        self.__meta = meta

    def get_id_increment(self, name: str, create: bool = False) -> int | None:
        if name not in self.__ids:
            if create:
                self.__ids[name] = 0
            else:
                return None

        self.__ids[name] = self.__ids[name] + 1
        return self.__ids[name]
