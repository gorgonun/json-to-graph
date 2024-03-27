from json2graph.id_manager import IdManager


class IdManagerApi():
    def __init__(self, actor_ref: IdManager):
        self.actor_ref = actor_ref

    async def get_id_increment(self, name: str, create: bool = False) -> int | None:
        return await self.actor_ref.get_id_increment.remote(name, create)
