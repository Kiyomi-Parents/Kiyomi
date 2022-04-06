from typing import List

import discord
from discord import SlashCommandGroup, Option, OptionChoice, ApplicationCommandInvokeError
from discord.commands import permissions

from src.kiyomi import Kiyomi
from .errors import SettingsCogException
from .services import SettingService
from .services.settings_autocomplete_service import SettingAutocompleteService
from .settings_cog import SettingsCog
from .storage import Setting


class Settings(SettingsCog):

    def __init__(self, bot: Kiyomi, setting_service: SettingService, settings_autocomplete_service: SettingAutocompleteService):
        super().__init__(bot, setting_service, settings_autocomplete_service)

        # Register events
        self.events()

    def events(self):
        @self.bot.events.on("setting_register")
        async def register_setting(settings: List[Setting]):
            self.setting_service.register_settings(settings)

    settings = SlashCommandGroup(
        "setting",
        "Various settings"
    )

    # Workaround
    async def get_settings(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        return self.settings_autocomplete_service.get_settings(ctx)

    async def get_setting_values(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        return await self.settings_autocomplete_service.get_setting_values(ctx)

    @settings.command(name="set", default_permission=False)
    @permissions.is_owner()
    async def settings_set(
        self,
        ctx: discord.ApplicationContext,
        setting: Option(
            str,
            "Setting name",
            autocomplete=get_settings
        ),
        value: Option(
            str,
            "Setting value",
            autocomplete=get_setting_values
        )
    ):
        """Set setting value"""

        abstract_setting = self.setting_service.set(ctx.interaction.guild.id, setting, value)
        setting_value = self.setting_service.get_value(ctx.interaction.guild.id, setting)

        await ctx.respond(f"{abstract_setting.name_human} is now set to: {setting_value}")

    @settings_set.error
    async def settings_set_error(self, ctx: discord.ApplicationContext, error: Exception):
        if isinstance(error, ApplicationCommandInvokeError):
            if isinstance(error.original, SettingsCogException):
                await ctx.respond(str(error.original))
                return
