from typing import Generic, TypeVar

import discord.ui

from src.kiyomi import Kiyomi

T = TypeVar('T', bound=discord.ui.View)


class BaseComponent(Generic[T]):
    def __init__(self, bot: Kiyomi, parent: T):
        self.bot = bot
        self.parent = parent
