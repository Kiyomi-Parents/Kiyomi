from abc import abstractmethod
from typing import Optional, Generic, TypeVar

from discord import Permissions

from .abstract_setting import AbstractSetting
from .setting import Setting
from src.kiyomi import Kiyomi

T = TypeVar("T")


class AbstractBotSetting(AbstractSetting[T], Generic[T]):
    bot: Kiyomi

    def __init__(
        self,
        bot: Kiyomi,
        name_human: str,
        setting: Setting,
        permissions: Optional[Permissions] = None,
    ):
        super().__init__(name_human, setting, permissions)

        self.bot = bot

    @staticmethod
    @abstractmethod
    async def is_valid(bot: Kiyomi, guild_id: int, value: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def create(
        bot: Kiyomi,
        name_human: str,
        name: str,
        permissions: Optional[Permissions] = None,
        default_value: Optional[T] = None,
    ):
        pass

    @staticmethod
    @abstractmethod
    def get_from_setting(
        bot: Kiyomi,
        name_human: str,
        setting: Setting,
        permissions: Optional[Permissions] = None,
    ):
        pass
