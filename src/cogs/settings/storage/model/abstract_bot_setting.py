from abc import abstractmethod
from typing import Optional, Generic, TypeVar

import discord

from .abstract_setting import AbstractSetting
from .setting import Setting
from src.kiyomi import Kiyomi

T = TypeVar('T')


class AbstractBotSetting(AbstractSetting[T], Generic[T]):

    bot: Kiyomi

    def __init__(self, bot: Kiyomi, name_human: str, setting: Setting):
        super().__init__(name_human, setting)

        self.bot = bot

    @staticmethod
    @abstractmethod
    def create(bot: Kiyomi, name_human: str, name: str, default_value: Optional[discord.abc.GuildChannel]):
        pass

    @staticmethod
    @abstractmethod
    def get_from_setting(bot: Kiyomi, name_human: str, setting: Setting):
        pass
