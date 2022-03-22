# Figure out default view
from abc import ABC, abstractmethod
from typing import Optional

import discord
from discord import Embed

from src.kiyomi import Kiyomi


class BaseView(discord.ui.View, ABC):
    def __init__(self, bot: Kiyomi):
        super().__init__(timeout=None)

        self.bot = bot

    def default_embed(self) -> Optional[Embed]:
        for child in self.children:
            get_embed = getattr(child, "get_embed", None)

            if callable(get_embed):
                return get_embed()
        # TODO: error embed
