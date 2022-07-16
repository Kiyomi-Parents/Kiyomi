import json
import random
from typing import List, Dict, Optional

from kiyomi.cogs.fancy_presence.storage.model.presence import Presence
from kiyomi.base_repository import BaseRepository, TEntity


class PresenceRepository(BaseRepository):
    @staticmethod
    def _load_file() -> List[Presence]:
        presences = []

        with open("src/cogs/fancy_presence/activities.json", "r") as file:
            for item in json.load(file):
                presences.append(Presence(**item))

        return presences

    async def get_by_id(self, entity_id: int) -> Optional[TEntity]:
        pass

    def get_all(self) -> List[Presence]:
        return self._load_file()

    async def exists(self, entity_id: int) -> bool:
        raise NotImplemented()

    async def add(self, entity: TEntity) -> TEntity:
        raise NotImplemented()

    async def add_all(self, entities: List[TEntity]) -> List[TEntity]:
        raise NotImplemented()

    async def remove(self, entity: TEntity) -> TEntity:
        raise NotImplemented()

    async def remove_by_id(self, entity_id: int) -> Optional[TEntity]:
        raise NotImplemented()

    async def upsert(self, entity: TEntity) -> TEntity:
        raise NotImplemented()

    async def update(self, entity_id: int, values: Dict[str, any]) -> TEntity:
        raise NotImplemented()

    async def update_entity(self, entity: TEntity) -> TEntity:
        raise NotImplemented()

    def get_random(self) -> Presence:
        presences = self.get_all()

        random_index = random.randint(0, len(presences) - 1)

        return presences[random_index]
