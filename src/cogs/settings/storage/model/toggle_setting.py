import distutils.util
from typing import overload, Optional

import discord
from discord import OptionChoice

from ...errors import InvalidSettingTypeException
from .setting import Setting
from .abstract_setting import AbstractSetting
from .enums.setting_type import SettingType


class ToggleSetting(AbstractSetting[bool]):

    def __init__(self, setting: Setting):
        self.setting = setting

    @staticmethod
    def create(name: str, default_value: Optional[bool]):
        if default_value is not None:
            default_value = ToggleSetting.from_type(default_value)

        return ToggleSetting(Setting(None, SettingType.BOOLEAN, name, default_value))

    @property
    def value(self) -> bool:
        return self.to_type(self.setting.value)

    @value.setter
    def value(self, value: bool):
        self.setting._value = self.from_type(value)

    @staticmethod
    def to_type(value: Optional[str]) -> Optional[bool]:
        if value is None:
            return None

        return distutils.util.strtobool(value)

    @staticmethod
    def from_type(value: Optional[bool]) -> Optional[str]:
        if value is None:
            return None

        return str(value)

    @staticmethod
    def get_from_setting(setting: Setting):
        if setting.setting_type is not SettingType.BOOLEAN:
            raise InvalidSettingTypeException(f"Can't convert setting of type {setting.setting_type} to {SettingType.BOOLEAN}")

        return ToggleSetting(setting)

    async def get_autocomplete(self, ctx: discord.AutocompleteContext):
        return [
            OptionChoice(f"Enabled{' (current)' if self.value else ''}", "True"),
            OptionChoice(f"Disabled{' (current)' if not self.value else ''}", "False")
        ]

