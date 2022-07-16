from typing import List

from discord import app_commands, Interaction
from discord.app_commands import Transform

from kiyomi import BaseCog
from .services import ServiceUnitOfWork
from .storage.model.abstract_setting import AbstractSetting
from .transformers.setting_name_transformer import SettingNameTransformer
from .transformers.setting_value_transformer import SettingValueTransformer


class Settings(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        @self.bot.events.on("setting_register")
        async def register_setting(settings: List[AbstractSetting]):
            self.service_uow.settings.register_settings(settings)
            await self.service_uow.close()

    settings = app_commands.Group(name="setting", description="Various settings", guild_only=True)

    @settings.command(name="set")
    @app_commands.describe(setting="Setting name", value="Setting value")
    async def settings_set(
        self,
        ctx: Interaction,
        setting: Transform[str, SettingNameTransformer],
        value: Transform[str, SettingValueTransformer],
    ):
        """Set setting value"""
        await ctx.response.defer(ephemeral=True)

        abstract_setting = await self.service_uow.settings.set(ctx.guild_id, setting, value)
        setting_value = await self.service_uow.settings.get_value(ctx.guild_id, setting)
        await self.service_uow.save_changes()

        await ctx.followup.send(
            f"{abstract_setting.name_human} is now set to: {setting_value}",
            ephemeral=True,
        )
