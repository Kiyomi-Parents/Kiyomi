from abc import ABC, abstractmethod
from typing import TypeVar, Generic

import discord
from discord import OptionChoice

from src.cogs.settings.storage.model import Setting
from src.cogs.settings.storage.model.enums.setting_type import SettingType

T = TypeVar('T')


class AbstractSetting(ABC, Generic[T]):

    setting: Setting

    def set(self, value: str) -> None:
        self.setting.value = value

    @property
    def value(self) -> T:
        return self.setting.value

    @value.setter
    def value(self, value: T) -> None:
        self.setting.value = value

    @property
    def name(self) -> str:
        return self.setting.name

    @property
    def type(self) -> SettingType:
        return self.setting.setting_type

    async def get_autocomplete(self, ctx: discord.AutocompleteContext):
        if self.setting.value is None:
            return []

        return [
            OptionChoice(f"{self.setting.value} (current)", self.setting.value)
        ]
