import random
import re
from typing import Optional

from discord import Emoji

from src.cogs.emoji_echo.errors import NotFound, AlreadyEnabled
from src.cogs.emoji_echo.services.emoji_echo_service import EmojiEchoService
from src.cogs.emoji_echo.storage.model.echo_emoji import EchoEmoji
from src.cogs.general import GeneralAPI


class EmojiService(EmojiEchoService):

    async def enable_emoji(self, guild_id: int, emoji_id: int, emoji_name: str) -> EchoEmoji:
        general = self.bot.get_cog_api(GeneralAPI)

        await general.register_emoji(guild_id, emoji_id, emoji_name)

        if self.uow.echo_emojis.get_by_emoji_id(emoji_id) is not None:
            raise AlreadyEnabled("Emoji is already enabled!")

        echo_emoji = self.uow.echo_emojis.add(EchoEmoji(emoji_id, guild_id))
        self.uow.save_changes()

        return echo_emoji

    async def disable_emoji(self, emoji_id: int):
        echo_emoji = self.uow.echo_emojis.get_by_emoji_id(emoji_id)

        if echo_emoji is None:
            raise NotFound(emoji_id)

        self.uow.echo_emojis.remove(echo_emoji)

        general = self.bot.get_cog_api(GeneralAPI)

        await general.unregister_emoji(echo_emoji.guild_id, emoji_id)

    def get_emoji_by_id(self, guild_id: int, emoji_id: int) -> Optional[Emoji]:
        echo_emoji = self.uow.echo_emojis.get_by_guild_id_and_emoji_id(guild_id, emoji_id)

        if echo_emoji is None:
            return None

        return self.bot.get_emoji(echo_emoji.emoji_id)

    def get_emoji_from_message(self, guild_id: int, msg: str):
        emoji_text = re.search(r'^<\w*:\w*:(\d*)>$', msg)

        if emoji_text is None:
            return None

        return self.get_emoji_by_id(guild_id, int(emoji_text.group(1)))

    async def get_random_enabled_emoji(self) -> Emoji:
        emoji_list = self.uow.echo_emojis.get_all()

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
