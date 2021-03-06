from typing import Optional, List

from discord import Member

from src.kiyomi import Kiyomi, Utils
from .settings_service import SettingsService
from ..errors import FailedToCreateSetting, \
    FailedToFindSetting, FailedToConvertSetting, InvalidSettingValue
from ..storage import Setting, SettingType, AbstractSetting, \
    UnitOfWork
from ..storage.model.abstract_bot_setting import AbstractBotSetting
from ..storage.model.abstract_regular_setting import AbstractRegularSetting


class SettingService(SettingsService):

    def __init__(self, bot: Kiyomi, uow: UnitOfWork):
        super().__init__(bot, uow)

        self.registered_settings: List[AbstractSetting] = []

    @staticmethod
    def convert_value_to_setting_type(value: any) -> SettingType:
        return SettingType(type(value))

    @staticmethod
    def convert_setting_type_to_value(setting_type: SettingType, value: str) -> any:
        return setting_type.value(value)

    def wrap_setting(self, name_human: str, setting: Setting) -> AbstractSetting:
        abstract_setting_classes = Utils.class_inheritors(AbstractSetting)
        setting_classes = []

        for abstract_setting_class in abstract_setting_classes:
            setting_classes += Utils.class_inheritors(abstract_setting_class)

        for setting_class in setting_classes:
            if issubclass(setting_class, AbstractSetting):
                if setting_class.setting_type is setting.setting_type:
                    if issubclass(setting_class, AbstractRegularSetting):
                        return setting_class.get_from_setting(name_human, setting)
                    elif issubclass(setting_class, AbstractBotSetting):
                        return setting_class.get_from_setting(self.bot, name_human, setting)

        raise FailedToConvertSetting(setting.setting_type)

    def has_permission(self, name: str, member: Member) -> bool:
        registered_setting = self.find_registered_setting(name)

        return registered_setting.has_permission(member)

    async def validate_setting_value(self, guild_id: int, name: str, value: Optional[str]):
        registered_setting = self.find_registered_setting(name)

        if isinstance(registered_setting, AbstractBotSetting):
            if not await registered_setting.is_valid(self.bot, guild_id, value):
                raise InvalidSettingValue(name, registered_setting.setting_type, value)
        elif isinstance(registered_setting, AbstractRegularSetting):
            if not await registered_setting.is_valid(value):
                raise InvalidSettingValue(name, registered_setting.setting_type, value)

    def find_registered_setting(self, name: str) -> AbstractSetting:
        for reg_setting in self.registered_settings:
            if reg_setting.name == name:
                return reg_setting

        raise FailedToFindSetting(name)

    def get(self, guild_id: int, name: str) -> AbstractSetting:
        registered_setting = self.find_registered_setting(name)
        setting = self.uow.settings_repo.get_by_guild_id_and_name(guild_id, name)

        if setting is not None:
            return self.wrap_setting(registered_setting.name_human, setting)
        else:
            new_setting = None

            if isinstance(registered_setting, AbstractBotSetting):
                new_setting = registered_setting.create(
                        self.bot,
                        registered_setting.name_human,
                        name,
                        registered_setting.value
                )
            elif isinstance(registered_setting, AbstractRegularSetting):
                new_setting = registered_setting.create(registered_setting.name_human, name, registered_setting.value)

            if new_setting is None:
                raise FailedToCreateSetting(name)

            new_setting.setting.guild_id = guild_id

            return new_setting

    def set(self, guild_id: int, name: str, value: Optional[any]) -> AbstractSetting:
        setting = self.get(guild_id, name)

        if setting.setting.id is None:
            setting.set(value)
            setting.setting = self.uow.settings_repo.add(setting.setting)
        else:
            self.uow.settings_repo.set(setting.setting, value)

        self.bot.events.emit("on_setting_change", setting)

        return setting

    def get_value(self, guild_id: int, name: str) -> Optional[any]:
        setting = self.get(guild_id, name)

        if setting is None:
            return None

        return setting.value

    def delete(self, guild_id: int, name: str) -> None:
        setting = self.get(guild_id, name)
        self.uow.settings_repo.remove(setting)

    def register_settings(self, settings: List[Setting]) -> None:
        self.registered_settings += settings
