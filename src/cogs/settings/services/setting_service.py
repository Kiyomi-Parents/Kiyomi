from typing import Optional, List

import discord
from discord import OptionChoice

from src.cogs.settings.utils import Utils
from src.kiyomi import Kiyomi
from .settings_service import SettingsService
from ..errors import SettingNotFoundException, FailedSettingConvertException
from ..storage import Setting, ChannelSetting, IntegerSetting, TextSetting, ToggleSetting, SettingType, AbstractSetting, \
    UnitOfWork
from ..storage.model.emoji_setting import EmojiSetting


class SettingService(SettingsService):

    def __init__(self, bot: Kiyomi, uow: UnitOfWork):
        super().__init__(bot, uow)

        self.registered_settings = []

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
        elif setting.setting_type is SettingType.EMOJI:
            return EmojiSetting.get_from_setting(bot, setting)
        else:
            raise FailedSettingConvertException(f"Unable to convert setting of type {setting.setting_type}")

    def get(self, guild_id: int, name: str) -> AbstractSetting:
        setting = self.uow.settings_repo.get_by_guild_id_and_name(guild_id, name)

        if setting is not None:
            return self.wrap_setting(self.bot, setting)
        else:
            for reg_setting in self.registered_settings:
                if reg_setting.name == name:
                    if isinstance(reg_setting, ChannelSetting) or isinstance(reg_setting, EmojiSetting):
                        new_setting = reg_setting.create(self.bot, name, reg_setting.value)
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
        self.registered_settings += settings

    def get_settings(self) -> List[OptionChoice]:
        settings = []

        for setting in self.registered_settings:
            settings.append(OptionChoice(Utils.snake_case_to_sentence(setting.name), setting.name))

        return settings

    async def get_setting_values(self, ctx: discord.AutocompleteContext):
        setting_name = ctx.options["setting"]
        setting = self.get(ctx.interaction.guild_id, setting_name)

        if setting is None:
            return []

        return await setting.get_autocomplete(ctx)
