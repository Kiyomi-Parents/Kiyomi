from typing import Type, List

from sqlalchemy import select

from ..model.channel import Channel
from src.kiyomi.database import BaseStorageRepository


class ChannelRepository(BaseStorageRepository[Channel]):
    @property
    def _table(self) -> Type[Channel]:
        return Channel

    async def get_all_by_guild_id(self, guild_id: int) -> List[Channel]:
        stmt = select(self._table).where(self._table.guild_id == guild_id)
        result = await self._execute_scalars(stmt)
        return result.all()
