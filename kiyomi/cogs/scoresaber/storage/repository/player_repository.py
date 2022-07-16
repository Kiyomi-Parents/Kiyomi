from typing import Type

from kiyomi.database import BaseStorageRepository
from ..model.player import Player


class PlayerRepository(BaseStorageRepository[Player]):
    @property
    def _table(self) -> Type[Player]:
        return Player