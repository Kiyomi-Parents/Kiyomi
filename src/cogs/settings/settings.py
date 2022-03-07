from typing import List

import discord
from discord import SlashCommandGroup, Option, OptionChoice

from src.kiyomi.base_cog import BaseCog
from .actions import Actions
from .storage.model import Setting
from .storage.uow import UnitOfWork


class Settings(BaseCog):

    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

        # Register events
        self.events()

    def events(self):
        @self.uow.bot.events.on("setting_register")
        async def register_setting(settings: List[Setting]):
            self.actions.register_settings(settings)

    settings = SlashCommandGroup(
        "setting",
        "Various settings"
    )

    # Workaround
    async def get_settings(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        return self.actions.get_settings()

    async def get_setting_values(self, ctx: discord.AutocompleteContext):
        return await self.actions.get_setting_values(ctx)

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
        registered_settings = [choice.value for choice in self.actions.get_settings()]

        if setting not in registered_settings:
            await ctx.respond(f"\"{setting}\" is not a valid setting name")

        self.actions.set(ctx.guild.id, setting, value)

        await ctx.respond(f"{setting} is now {value}")

