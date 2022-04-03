import random
import re
from typing import List, Optional

import discord
from discord import OptionChoice

from .general_service import GeneralService
from ..errors import EmojiAlreadyExistsException, EmojiNotFoundException
from ..storage.model.emoji import Emoji


class EmojiService(GeneralService):
    @staticmethod
    def find_all_emoji_by_name(name: str, emojis: List[OptionChoice]) -> List[OptionChoice]:
        return [
            emoji
            for emoji in emojis
            if emoji.name.startswith(name.lower())
        ]

    async def get_available_emojis(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        enabled_emojis = self.uow.emojis.get_by_guild_id(ctx.interaction.guild_id)
        emojis = []

        for emoji in ctx.bot.emojis:
            if emoji.id in [enabled_emoji.id for enabled_emoji in enabled_emojis]:
                continue

            emojis.append(discord.OptionChoice(emoji.name, str(emoji.id)))

        return self.find_all_emoji_by_name(ctx.value.lower(), emojis)

    async def get_enabled_emojis(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        enabled_emojis = self.uow.emojis.get_by_guild_id(ctx.interaction.guild_id)
        emojis = []

        for emoji in enabled_emojis:
            emojis.append(discord.OptionChoice(emoji.name, str(emoji.id)))

        return self.find_all_emoji_by_name(ctx.value.lower(), emojis)

    async def enable_emoji(self, emoji_id: int, guild_id: int, emoji_name: str):
        if self.uow.emojis.get_by_id(emoji_id) is not None:
            raise EmojiAlreadyExistsException("Emoji is already enabled!")

        self.uow.emojis.add(Emoji(emoji_id, guild_id, emoji_name))

    async def disable_emoji(self, emoji_id: int):
        emoji = self.uow.emojis.get_by_id(emoji_id)

        if emoji is None:
            raise EmojiNotFoundException("Emoji is already disabled!")

        self.uow.emojis.remove(emoji)

    def get_emoji_by_id(self, emoji_id: int) -> Optional[Emoji]:
        emoji = self.uow.emojis.get_by_id(emoji_id)

        if emoji is None:
            return None

        return self.bot.get_emoji(emoji.id)

    def get_emoji_from_message(self, msg: str):
        emoji_text = re.search(r'^<\w*:\w*:(\d*)>$', msg)

        if emoji_text is None:
            return None

        return self.get_emoji_by_id(int(emoji_text.group(1)))

    async def get_random_enabled_emoji(self):
        emoji_list = self.uow.emojis.get_all()
        emoji = None

        for i in range(10):
            test_emoji = emoji_list[random.randint(0, len(emoji_list) - 1)]
            emoji = self.bot.get_emoji(test_emoji.id)

            if emoji is not None:
                break

        return emoji