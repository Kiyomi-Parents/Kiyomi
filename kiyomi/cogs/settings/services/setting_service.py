from typing import Optional, List, Any

import discord

from kiyomi import Kiyomi, Utils, BaseService
from ..errors import (
    FailedToCreateSetting,
    FailedToFindSetting,
    FailedToConvertSetting,
    InvalidSettingValue,
)
from ..storage import StorageUnitOfWork
from ..storage.model.abstract_bot_setting import AbstractBotSetting
from ..storage.model.abstract_regular_setting import AbstractRegularSetting
from ..storage.model.abstract_setting import AbstractSetting
from ..storage.model.enums.setting_type import SettingType
from ..storage.model.setting import Setting
from ..storage.repository.settings_repository import SettingRepository


class SettingService(BaseService[Setting, SettingRepository, StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, repository: SettingRepository, storage_uow: StorageUnitOfWork):
        super().__init__(bot, repository, storage_uow)

        self.registered_settings: List[AbstractSetting] = []

    @staticmethod
    def convert_value_to_setting_type(value: Any) -> SettingType:
        return SettingType(type(value))

    @staticmethod
    def convert_setting_type_to_value(setting_type: SettingType, value: str) -> Any:
        return setting_type.value(value)

    def wrap_setting(self, group: str, name_human: str, setting: Setting) -> AbstractSetting:
        abstract_setting_classes = Utils.class_inheritors(AbstractSetting)
        setting_classes = []

        for abstract_setting_class in abstract_setting_classes:
            setting_classes += Utils.class_inheritors(abstract_setting_class)

        for setting_class in setting_classes:
            if issubclass(setting_class, AbstractSetting):
                if setting_class.setting_type is setting.setting_type:
                    if issubclass(setting_class, AbstractRegularSetting):
                        return setting_class.get_from_setting(group, name_human, setting)
                    elif issubclass(setting_class, AbstractBotSetting):
                        return setting_class.get_from_setting(self.bot, group, name_human, setting)

        raise FailedToConvertSetting(setting.setting_type)

    def has_permission(self, name: str, discord_member: discord.Member) -> bool:
        registered_setting = self.find_registered_setting(name)

        return registered_setting.has_permission(discord_member)

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

    async def get(self, guild_id: int, name: str) -> AbstractSetting:
        registered_setting = self.find_registered_setting(name)
        setting = await self.repository.get_by_guild_id_and_name(guild_id, name)

        if setting is not None:
            return self.wrap_setting(registered_setting.group, registered_setting.name_human, setting)
        else:
            new_setting = None

            if isinstance(registered_setting, AbstractBotSetting):
                new_setting = registered_setting.create(
                    self.bot,
                    registered_setting.group,
                    registered_setting.name_human,
                    name,
                    registered_setting.value,
                )
            elif isinstance(registered_setting, AbstractRegularSetting):
                new_setting = registered_setting.create(registered_setting.group, registered_setting.name_human, name,
                                                        registered_setting.value)

            if new_setting is None:
                raise FailedToCreateSetting(name)

            new_setting.setting.guild_id = guild_id

            return new_setting

    async def set(self, guild_id: int, name: str, value: Optional[Any]) -> AbstractSetting:
        setting = await self.get(guild_id, name)

        if setting.setting.id is None:
            setting.set(value)
            setting.setting = await self.repository.add(setting.setting)
        else:
            await self.repository.set(setting.setting.id, value)

        self.bot.events.emit("on_setting_change", setting)

        return setting

    async def get_value(self, guild_id: int, name: str) -> Optional[Any]:
        setting = await self.get(guild_id, name)

        if setting is None:
            return None

        return setting.value

    async def delete(self, guild_id: int, name: str) -> AbstractSetting:
        setting = await self.get(guild_id, name)
        await self.repository.remove_by_id(setting.setting.id)
        return setting

    def register_settings(self, settings: List[AbstractSetting]) -> None:
        self.registered_settings += settings
