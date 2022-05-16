from typing import Type

from src.kiyomi.database import BaseRepository
from ..model.player import Player


class PlayerRepository(BaseRepository[Player]):

    @property
    def _table(self) -> Type[Player]:
        return Player
