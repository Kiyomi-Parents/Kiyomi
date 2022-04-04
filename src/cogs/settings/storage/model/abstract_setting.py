from abc import ABC
from typing import TypeVar, Generic

import discord
from discord import OptionChoice

from .enums.setting_type import SettingType
from .setting import Setting

T = TypeVar('T')


class AbstractSetting(ABC, Generic[T]):
    setting_type: SettingType
    setting: Setting

    def __init__(self, name_human: str, setting: Setting):
        self.setting = setting
        self.name_human = name_human

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

    @property
    def guild_id(self) -> int:
        return self.setting.guild_id

    async def get_autocomplete(self, ctx: discord.AutocompleteContext):
        if self.setting.value is None:
            return []

        return [
            OptionChoice(f"{self.setting.value} (current)", self.setting.value)
        ]
