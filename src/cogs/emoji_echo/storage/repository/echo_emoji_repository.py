from typing import Optional, List, Type

from sqlalchemy import select

from src.cogs.emoji_echo.storage.model.echo_emoji import EchoEmoji
from src.kiyomi import BaseStorageRepository


class EchoEmojiRepository(BaseStorageRepository[EchoEmoji]):
    @property
    def _table(self) -> Type[EchoEmoji]:
        return EchoEmoji

    async def get_by_emoji_id(self, emoji_id: int) -> Optional[EchoEmoji]:
        stmt = select(self._table).where(self._table.emoji_id == emoji_id)
        return await self._first(stmt)

    async def get_by_guild_id(self, guild_id: int) -> List[EchoEmoji]:
        stmt = select(self._table).where(self._table.guild_id == guild_id)
        return await self._all(stmt)

    async def get_by_guild_id_and_emoji_id(self, guild_id: int, emoji_id: int) -> Optional[EchoEmoji]:
        stmt = select(self._table).where(self._table.guild_id == guild_id).where(self._table.emoji_id == emoji_id)
        return await self._first(stmt)
