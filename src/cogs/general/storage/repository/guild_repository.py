from typing import Type

from ..model.guild import Guild
from src.kiyomi.database import BaseRepository


class GuildRepository(BaseRepository[Guild]):
    @property
    def _table(self) -> Type[Guild]:
        return Guild
