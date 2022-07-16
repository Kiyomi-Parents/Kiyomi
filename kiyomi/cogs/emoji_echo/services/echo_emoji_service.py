import random
import re
from typing import Optional

from discord import Emoji

from kiyomi.cogs.general import GeneralAPI
from ..storage import StorageUnitOfWork
from ..errors import NotFound, AlreadyEnabled
from ..storage.model.echo_emoji import EchoEmoji
from kiyomi import BaseService
from ..storage.repository.echo_emoji_repository import EchoEmojiRepository


class EchoEmojiService(BaseService[EchoEmoji, EchoEmojiRepository, StorageUnitOfWork]):
    async def enable_emoji(self, guild_id: int, emoji_id: int, emoji_name: str) -> EchoEmoji:
        general = self.bot.get_cog_api(GeneralAPI)

        await general.register_emoji(guild_id, emoji_id, emoji_name)

        if await self.storage_uow.echo_emojis.exists(emoji_id):
            raise AlreadyEnabled("Emoji is already enabled!")

        return await self.storage_uow.echo_emojis.add(EchoEmoji(emoji_id, guild_id))

    async def disable_emoji(self, emoji_id: int) -> Optional[EchoEmoji]:
        echo_emoji = await self.storage_uow.echo_emojis.remove_by_id(emoji_id)

        if echo_emoji is None:
            return None

        general = self.bot.get_cog_api(GeneralAPI)

        await general.unregister_emoji(echo_emoji.guild_id, emoji_id)
        return echo_emoji

    async def get_emoji_by_id(self, guild_id: int, emoji_id: int) -> Optional[Emoji]:
        echo_emoji = await self.storage_uow.echo_emojis.get_by_guild_id_and_emoji_id(guild_id, emoji_id)

        if echo_emoji is None:
            return None

        return self.bot.get_emoji(echo_emoji.emoji_id)

    async def get_emoji_from_message(self, guild_id: int, msg: str):
        emoji_text = re.search(r"^<\w*:\w*:(\d*)>$", msg)

        if emoji_text is None:
            return None

        return await self.get_emoji_by_id(guild_id, int(emoji_text.group(1)))

    async def get_random_enabled_emoji(self) -> Emoji:
        emoji_list = await self.storage_uow.echo_emojis.get_all()

        if len(emoji_list) <= 0:
            raise NotFound()

        emoji = None

        for i in range(10):
            test_emoji = emoji_list[random.randint(0, len(emoji_list) - 1)]
            emoji = self.bot.get_emoji(test_emoji.emoji_id)

            if emoji is not None:
                break

        if emoji is None:
            raise NotFound()

        return emoji
