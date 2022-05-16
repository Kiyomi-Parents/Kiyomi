from typing import List

from .services.emoji_service import EmojiService
from .storage.unit_of_work import UnitOfWork
from .emoji_echo_cog import EmojiEchoCog
from .storage.model.echo_emoji import EchoEmoji
from src.kiyomi import Kiyomi


class EmojiEchoAPI(EmojiEchoCog):
    def __init__(
            self,
            bot: Kiyomi,
            emoji_service: EmojiService,
            uow: UnitOfWork
    ):
        super().__init__(bot, emoji_service)

        self.uow = uow

    async def get_enabled_emojis(self, guild_id: int) -> List[EchoEmoji]:
        return await self.uow.echo_emojis.get_by_guild_id(guild_id)
