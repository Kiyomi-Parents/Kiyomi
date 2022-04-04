from abc import abstractmethod
from typing import Optional, Generic, TypeVar

import discord

from .abstract_setting import AbstractSetting
from .setting import Setting

T = TypeVar('T')


class AbstractRegularSetting(AbstractSetting[T], Generic[T]):

    @staticmethod
    @abstractmethod
    def create(name_human: str, name: str, default_value: Optional[discord.abc.GuildChannel]):
        pass

    @staticmethod
    @abstractmethod
    def get_from_setting(name_human: str, setting: Setting):
        pass
