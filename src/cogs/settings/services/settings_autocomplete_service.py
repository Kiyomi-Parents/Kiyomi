from typing import List

import discord
from discord import OptionChoice

from .setting_service import SettingService
from ..errors import SettingsCogException
from ..storage import UnitOfWork
from .settings_service import SettingsService
from src.kiyomi import Kiyomi


class SettingAutocompleteService(SettingsService):

    def __init__(self, bot: Kiyomi, uow: UnitOfWork, setting_service: SettingService):
        super().__init__(bot, uow)

        self.setting_service = setting_service

    def get_settings(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        settings = []

        for setting in self.setting_service.registered_settings:

            if not setting.has_permission(ctx.interaction.user):
                continue

            if ctx.value.lower() in setting.name_human.lower():
                settings.append(OptionChoice(setting.name_human, setting.name))

        return settings

    async def get_setting_values(self, ctx: discord.AutocompleteContext):
        setting_name = ctx.options["setting"]

        try:
            setting = self.setting_service.get(ctx.interaction.guild_id, setting_name)
        except SettingsCogException:
            return []

        if setting is None:
            return []

        if not setting.has_permission(ctx.interaction.user):
            return []

        return await setting.get_autocomplete(ctx)
