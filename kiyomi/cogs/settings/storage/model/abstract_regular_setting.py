from abc import abstractmethod
from typing import Optional, Generic, TypeVar

from discord import Permissions

from .abstract_setting import AbstractSetting
from .setting import Setting

T = TypeVar("T")


class AbstractRegularSetting(AbstractSetting[T], Generic[T]):
    @staticmethod
    @abstractmethod
    async def is_valid(value: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def create(
        group: str,
        name_human: str,
        name: str,
        permissions: Optional[Permissions] = None,
        default_value: Optional[T] = None,
    ):
        pass

    @staticmethod
    @abstractmethod
    def get_from_setting(group: str, name_human: str, setting: Setting, permissions: Optional[Permissions] = None):
        pass
