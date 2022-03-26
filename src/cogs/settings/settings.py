from typing import List

import discord
from discord import SlashCommandGroup, Option, OptionChoice

from src.kiyomi import Kiyomi
from .services import SettingService
from .settings_cog import SettingsCog
from .storage import Setting


class Settings(SettingsCog):

    def __init__(self, bot: Kiyomi, setting_service: SettingService):
        super().__init__(bot, setting_service)

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
        return self.setting_service.get_settings()

    async def get_setting_values(self, ctx: discord.AutocompleteContext):
        return await self.setting_service.get_setting_values(ctx)

    # TODO: Fix auto complete support for partially typed setting names
    @settings.command(name="set")
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
        registered_settings = [choice.value for choice in self.setting_service.get_settings()]

        if setting not in registered_settings:
            await ctx.respond(f"\"{setting}\" is not a valid setting name")

        self.setting_service.set(ctx.interaction.guild.id, setting, value)
        setting_value = self.setting_service.get_value(ctx.interaction.guild.id, setting)

        await ctx.respond(f"{setting} is now set to: {setting_value}")

