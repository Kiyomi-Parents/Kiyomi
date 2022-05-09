from typing import Optional, List, Type

from sqlalchemy import select, delete

from ..model.emoji import Emoji
from src.kiyomi.database import BaseRepository


class EmojiRepository(BaseRepository[Emoji]):
    @property
    def _table(self) -> Type[Emoji]:
        return Emoji

    async def get_by_name(self, emoji_name: str) -> Optional[Emoji]:
        stmt = select(self._table).where(self._table.name == emoji_name)
        result = await self._execute_scalars(stmt)
        return result.first()

    async def get_by_guild_id(self, guild_id: int) -> List[Emoji]:
        stmt = select(self._table).where(self._table.guild_id == guild_id)
        result = await self._execute_scalars(stmt)
        return result.all()

    async def get_by_guild_id_and_id(self, guild_id: int, emoji_id: int) -> Optional[Emoji]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.id == emoji_id)
        result = await self._execute_scalars(stmt)
        return result.first()

    async def delete_by_guild_id_and_id(self, guild_id: int, emoji_id: int):
        stmt = delete(self._table).where(self._table.guild_id == guild_id).where(self._table.id == emoji_id)
        await self._session.execute(stmt)
