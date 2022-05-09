from src.kiyomi import Kiyomi
from .general_service import GeneralService
from .guild_service import GuildService
from ..storage import UnitOfWork
from ..storage.model.emoji import Emoji


class EmojiService(GeneralService):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, guild_service: GuildService):
        super().__init__(bot, uow)

        self.guild_service = guild_service

    async def register_emoji(self, guild_id: int, emoji_id: int, emoji_name: str) -> Emoji:
        async with self.uow:
            await self.guild_service.register_guild(guild_id)

            return await self.uow.emojis.add(Emoji(guild_id, emoji_id, emoji_name))

    async def unregister_emoji(self, guild_id: int, emoji_id: int):
        async with self.uow:
            self.uow.emojis.delete_by_guild_id_and_id(guild_id, emoji_id)
