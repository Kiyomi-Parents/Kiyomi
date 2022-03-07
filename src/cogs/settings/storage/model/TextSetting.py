from typing import Optional

from src.cogs.settings.errors import InvalidSettingTypeException
from src.cogs.settings.storage.model import Setting
from src.cogs.settings.storage.model.AbstractSetting import AbstractSetting
from src.cogs.settings.storage.model.enums.setting_type import SettingType


class TextSetting(AbstractSetting[str]):

    def __init__(self, setting: Setting):
        self.setting = setting

    @staticmethod
    def create(name: str, default_value: Optional[str]):
        if default_value is not None:
            default_value = TextSetting.from_type(default_value)

        return TextSetting(Setting(None, SettingType.STRING, name, default_value))

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
    def get_from_setting(setting: Setting):
        if setting.setting_type is not SettingType.STRING:
            raise InvalidSettingTypeException(f"Can't convert setting of type {setting.setting_type} to {SettingType.STRING}")

        return TextSetting(setting)
