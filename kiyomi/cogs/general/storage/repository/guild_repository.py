from typing import Type

from ..model.guild import Guild
from kiyomi.database import BaseStorageRepository


class GuildRepository(BaseStorageRepository[Guild]):
    @property
    def _table(self) -> Type[Guild]:
        return Guild
