from typing import Optional, List, Union

import discord
from discord import Interaction
from discord.app_commands import Transformer, Choice
from discord.ext.commands import Context, EmojiConverter

from src.cogs.emoji_echo.emoji_echo_api import EmojiEchoAPI


class AvailableEmojiTransformer(Transformer):
    @classmethod
    async def transform(cls, interaction: Interaction, value: str) -> Optional[discord.Emoji]:
        ctx = await Context.from_interaction(interaction)
        return await EmojiConverter().convert(ctx, value)

    @classmethod
    async def autocomplete(
            cls,
            interaction: Interaction,
            value: Union[int, float, str]
    ) -> List[Choice[Union[int, float, str]]]:
        ctx = await Context.from_interaction(interaction)
        echo_emojis = ctx.bot.get_cog_api(EmojiEchoAPI)

        enabled_emojis = echo_emojis.get_enabled_emojis(interaction.guild_id)
        emojis = []

        for emoji in enabled_emojis:
            if emoji.name.startswith(value.lower()):
                continue

            emojis.append(Choice(name=emoji.name, value=str(emoji.id)))

        return emojis
