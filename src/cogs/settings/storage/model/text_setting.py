from typing import Optional

from discord import Permissions

from .abstract_regular_setting import AbstractRegularSetting
from .enums.setting_type import SettingType
from .setting import Setting
from ...errors import InvalidSettingType


class TextSetting(AbstractRegularSetting[str]):
    setting_type = SettingType.STRING

    @staticmethod
    def create(
            name_human: str,
            name: str,
            permissions: Optional[Permissions] = None,
            default_value: Optional[str] = None
    ):
        if default_value is not None:
            default_value = TextSetting.from_type(default_value)

        return TextSetting(
                name_human,
                Setting(None, SettingType.STRING, name, default_value),
                permissions
        )

    @property
    def value(self) -> str:
        return self.setting.value

    @value.setter
    def value(self, value: str):
        self.setting.value = value.lower()

    @staticmethod
    def to_type(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        return value

    @staticmethod
    def from_type(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        return value

    @staticmethod
    def get_from_setting(
            name_human: str,
            setting: Setting,
            permissions: Optional[Permissions] = None
    ):
        if setting.setting_type is not SettingType.STRING:
            raise InvalidSettingType(setting.setting_type, SettingType.STRING)

        return TextSetting(name_human, setting, permissions)

    @staticmethod
    async def is_valid(value: str) -> bool:
        return isinstance(value, str)
