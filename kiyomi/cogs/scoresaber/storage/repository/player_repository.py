from typing import Type, List

from sqlalchemy import select
from sqlalchemy.orm import noload

from kiyomi.database import BaseStorageRepository
from ..model.player import Player


class PlayerRepository(BaseStorageRepository[Player]):
    @property
    def _table(self) -> Type[Player]:
        return Player

    async def get_all_player_ids(self) -> List[int]:
        stmt = select(self._table.id).options(noload("*"))
        return await self._all(stmt)

    async def get_all_player(self) -> List[Player]:
        stmt = select(self._table).options(noload("*"))
        return await self._all(stmt)
    