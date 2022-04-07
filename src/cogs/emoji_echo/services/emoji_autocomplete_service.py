from typing import List

import discord
from discord import OptionChoice

from src.cogs.emoji_echo.services.emoji_echo_service import EmojiEchoService


class EmojiAutocompleteService(EmojiEchoService):
    @staticmethod
    def find_all_emoji_by_name(name: str, emojis: List[OptionChoice]) -> List[OptionChoice]:
        return [
            emoji
            for emoji in emojis
            if emoji.name.startswith(name.lower())
        ]

    async def get_available_emojis(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        enabled_emojis = self.uow.echo_emojis.get_by_guild_id(ctx.interaction.guild_id)
        emojis = []

        for emoji in ctx.interaction.guild.emojis:
            if emoji.id in [enabled_emoji.emoji_id for enabled_emoji in enabled_emojis]:
                continue

            emojis.append(discord.OptionChoice(emoji.name, str(emoji.id)))

        return self.find_all_emoji_by_name(ctx.value.lower(), emojis)

    async def get_enabled_emojis(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        enabled_emojis = self.uow.echo_emojis.get_by_guild_id(ctx.interaction.guild_id)
        emojis = []

        for emoji in enabled_emojis:
            emojis.append(discord.OptionChoice(emoji.emoji.name, str(emoji.emoji_id)))

        return self.find_all_emoji_by_name(ctx.value.lower(), emojis)
