from kiyomi import BaseService
from ..storage import StorageUnitOfWork
from ..storage.model.emoji import Emoji
from ..storage.repository.emoji_repository import EmojiRepository


class EmojiService(BaseService[Emoji, EmojiRepository, StorageUnitOfWork]):
    async def register_emoji(self, guild_id: int, emoji_id: int, emoji_name: str) -> Emoji:
        return await self.repository.add(Emoji(guild_id, emoji_id, emoji_name))

    async def unregister_emoji(self, guild_id: int, emoji_id: int):
        await self.repository.delete_by_guild_id_and_id(guild_id, emoji_id)
