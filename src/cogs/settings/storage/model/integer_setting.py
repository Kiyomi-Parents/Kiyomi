from typing import Optional

from discord import Permissions

from .abstract_regular_setting import AbstractRegularSetting
from .enums.setting_type import SettingType
from .setting import Setting
from ...errors import InvalidSettingType


class IntegerSetting(AbstractRegularSetting[int]):
    setting_type = SettingType.INT

    @staticmethod
    def create(
            name_human: str,
            name: str,
            permissions: Optional[Permissions] = None,
            default_value: Optional[int] = None
    ):
        if default_value is not None:
            default_value = IntegerSetting.from_type(default_value)

        return IntegerSetting(
                name_human,
                Setting(None, SettingType.INT, name, default_value),
                permissions
        )

    @property
    def value(self) -> int:
        return self.to_type(self.setting.value)

    @value.setter
    def value(self, value: int):
        self.setting.value = self.from_type(value)

    @staticmethod
    def to_type(value: Optional[str]) -> Optional[int]:
        if value is None:
            return None

        return int(value)

    @staticmethod
    def from_type(value: Optional[int]) -> Optional[str]:
        if value is None:
            return None

        return str(value)

    @staticmethod
    def get_from_setting(
            name_human: str,
            setting: Setting,
            permissions: Optional[Permissions] = None
    ):
        if setting.setting_type is not SettingType.INT:
            raise InvalidSettingType(setting.setting_type, SettingType.INT)

        return IntegerSetting(name_human, setting, permissions)

    @staticmethod
    async def is_valid(value: str) -> bool:
        return value.isdigit()
