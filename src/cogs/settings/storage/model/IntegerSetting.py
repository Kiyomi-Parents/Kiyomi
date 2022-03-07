from typing import overload, Optional

from src.cogs.settings.errors import InvalidSettingTypeException
from src.cogs.settings.storage.model import Setting
from src.cogs.settings.storage.model.AbstractSetting import AbstractSetting
from src.cogs.settings.storage.model.enums.setting_type import SettingType


class IntegerSetting(AbstractSetting[int]):

    def __init__(self, setting: Setting):
        self.setting = setting

    @staticmethod
    def create(name: str, default_value: Optional[int]):
        if default_value is not None:
            default_value = IntegerSetting.from_type(default_value)

        return IntegerSetting(Setting(None, SettingType.INT, name, default_value))

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
    def get_from_setting(setting: Setting):
        if setting.setting_type is not SettingType.INT:
            raise InvalidSettingTypeException(f"Can't convert setting of type {setting.setting_type} to {SettingType.INT}")

        return IntegerSetting(setting)
