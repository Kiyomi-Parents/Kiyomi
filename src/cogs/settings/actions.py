import distutils.util
from typing import Optional

from src.cogs.settings.storage.model import Setting
from src.cogs.settings.storage.model.enums.setting_type import SettingType


class Actions:
    def __init__(self, uow):
        self.uow = uow

    @staticmethod
    def convert_value_to_setting_type(value: any) -> SettingType:
        return SettingType(type(value))

    @staticmethod
    def convert_setting_type_to_value(setting_type: SettingType, value: str) -> any:
        if setting_type.value == bool:
            return distutils.util.strtobool(value)

        return setting_type.value(value)

    def get(self, guild_id: int, name: str) -> Optional[Setting]:
        return self.uow.settings_repo.find(guild_id, name)

    def set(self, guild_id: int, name: str, value: any) -> None:
        setting = self.get(guild_id, name)

        if setting is None:
            setting_type = self.convert_value_to_setting_type(value)
            setting = self.uow.settings_repo.add(Setting(guild_id, setting_type, name, str(value)))
        else:
            self.uow.settings_repo.set(setting, str(value))

    def get_value(self, guild_id: int, name: str) -> Optional[any]:
        setting = self.get(guild_id, name)

        if setting is None:
            return None

        return self.convert_setting_type_to_value(setting.setting_type, setting.value)

    def delete(self, guild_id: int, name: str) -> None:
        setting = self.get(guild_id, name)
        self.uow.settings_repo.remove(setting)
