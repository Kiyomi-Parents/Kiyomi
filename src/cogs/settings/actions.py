from typing import Optional, List

import discord
from discord import OptionChoice

from .errors import SettingNotFoundException, FailedSettingConvertException
from .storage.model import Setting
from .storage.model.AbstractSetting import AbstractSetting
from .storage.model.ChannelSetting import ChannelSetting
from .storage.model.IntegerSetting import IntegerSetting
from .storage.model.TextSetting import TextSetting
from .storage.model.ToggleSetting import ToggleSetting
from .storage.model.enums.setting_type import SettingType
from .storage.uow import UnitOfWork
from .utils import Utils


class Actions:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

        self.settings = []

    @staticmethod
    def convert_value_to_setting_type(value: any) -> SettingType:
        return SettingType(type(value))

    @staticmethod
    def convert_setting_type_to_value(setting_type: SettingType, value: str) -> any:
        return setting_type.value(value)

    @staticmethod
    def wrap_setting(bot: discord.abc, setting: Setting):
        if setting.setting_type is SettingType.BOOLEAN:
            return ToggleSetting.get_from_setting(setting)
        elif setting.setting_type is SettingType.INT:
            return IntegerSetting.get_from_setting(setting)
        elif setting.setting_type is SettingType.STRING:
            return TextSetting.get_from_setting(setting)
        elif setting.setting_type is SettingType.CHANNEL:
            return ChannelSetting.get_from_setting(bot, setting)
        else:
            raise FailedSettingConvertException(f"Unable to convert setting of type {setting.setting_type}")

    def get(self, guild_id: int, name: str) -> AbstractSetting:
        setting = self.uow.settings_repo.find(guild_id, name)

        if setting is not None:
            return self.wrap_setting(self.uow.bot, setting)
        else:
            for reg_setting in self.settings:
                if reg_setting.name == name:
                    if isinstance(reg_setting, ChannelSetting):
                        new_setting = reg_setting.create(self.uow.bot, name, reg_setting.value)
                    else:
                        new_setting = reg_setting.create(name, reg_setting.value)

                    new_setting.setting.guild_id = guild_id

                    return new_setting

        raise SettingNotFoundException(f"Could not find setting with name: {name}")

    def set(self, guild_id: int, name: str, value: Optional[any]) -> None:
        setting = self.get(guild_id, name)

        if setting.setting.id is None:
            setting.set(value)
            setting.setting = self.uow.settings_repo.add(setting.setting)
        else:
            self.uow.settings_repo.set(setting.setting, value)

    def get_value(self, guild_id: int, name: str) -> Optional[any]:
        setting = self.get(guild_id, name)

        if setting is None:
            return None

        return setting.value

    def delete(self, guild_id: int, name: str) -> None:
        setting = self.get(guild_id, name)
        self.uow.settings_repo.remove(setting)

    def register_settings(self, settings: List[Setting]) -> None:
        self.settings += settings

    def get_settings(self) -> List[OptionChoice]:
        settings = []

        for setting in self.settings:

            settings.append(OptionChoice(Utils.snake_case_to_sentence(setting.name), setting.name))

        return settings

    async def get_setting_values(self, ctx: discord.AutocompleteContext):
        setting_name = ctx.options["setting"]
        setting = self.get(ctx.interaction.guild_id, setting_name)

        if setting is None:
            return []

        return await setting.get_autocomplete(ctx)
