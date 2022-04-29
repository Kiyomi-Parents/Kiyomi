from typing import List

from discord import Interaction
from discord.app_commands import Choice

from .setting_service import SettingService
from ..errors import SettingsCogException
from ..storage import UnitOfWork
from .settings_service import SettingsService
from src.kiyomi import Kiyomi


class SettingAutocompleteService(SettingsService):

    def __init__(self, bot: Kiyomi, uow: UnitOfWork, setting_service: SettingService):
        super().__init__(bot, uow)

        self.setting_service = setting_service

    def get_settings(self, ctx: Interaction, current: str) -> List[Choice]:
        settings = []

        for setting in self.setting_service.registered_settings:

            if not setting.has_permission(ctx.user):
                continue

            if current.lower() in setting.name_human.lower():
                settings.append(Choice(name=setting.name_human, value=setting.name))

        return settings

    async def get_setting_values(self, ctx: Interaction, current: str):
        setting_name = ctx.namespace.setting

        try:
            setting = self.setting_service.get(ctx.guild_id, setting_name)
        except SettingsCogException:
            return []

        if setting is None:
            return []

        if not setting.has_permission(ctx.user):
            return []

        return await setting.get_autocomplete(ctx, current)
