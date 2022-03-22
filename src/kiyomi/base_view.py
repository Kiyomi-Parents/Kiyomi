# Figure out default view
from abc import ABC, abstractmethod
from typing import Optional

import discord
from discord import Embed, Guild

from src.kiyomi import Kiyomi


class BaseView(discord.ui.View, ABC):
    def __init__(self, bot: Kiyomi, guild: Guild):
        super().__init__(timeout=None)

        self.bot = bot
        self.guild = guild

    def default_embed(self) -> Optional[Embed]:
        for child in self.children:
            get_embed = getattr(child, "get_embed", None)

            if callable(get_embed):
                return get_embed()
        # TODO: error embed
