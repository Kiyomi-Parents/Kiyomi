import distutils.util
from typing import Optional

import discord
from discord import OptionChoice

from .abstract_regular_setting import AbstractRegularSetting
from .enums.setting_type import SettingType
from .setting import Setting
from ...errors import InvalidSettingType


class ToggleSetting(AbstractRegularSetting[bool]):
    setting_type = SettingType.BOOLEAN

    @staticmethod
    def create(name_human: str, name: str, default_value: Optional[bool]):
        if default_value is not None:
            default_value = ToggleSetting.from_type(default_value)

        return ToggleSetting(name_human, Setting(None, SettingType.BOOLEAN, name, default_value))

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
    def get_from_setting(name_human: str, setting: Setting):
        if setting.setting_type is not SettingType.BOOLEAN:
            raise InvalidSettingType(setting.setting_type, SettingType.BOOLEAN)

        return ToggleSetting(name_human, setting)

    async def get_autocomplete(self, ctx: discord.AutocompleteContext):
        return [
            OptionChoice(f"Enabled{' (current)' if self.value else ''}", "True"),
            OptionChoice(f"Disabled{' (current)' if not self.value else ''}", "False")
        ]

