from typing import List

from discord import app_commands, Interaction
from discord.app_commands import Transform

from src.kiyomi import Kiyomi
from .services import SettingService
from .settings_cog import SettingsCog
from .storage import Setting
from .transformers.setting_name_transformer import SettingNameTransformer
from .transformers.setting_value_transformer import SettingValueTransformer


class Settings(SettingsCog):

    def __init__(
            self,
            bot: Kiyomi,
            setting_service: SettingService
    ):
        super().__init__(bot, setting_service)

        # Register events
        self.events()

    def events(self):
        @self.bot.events.on("setting_register")
        async def register_setting(settings: List[Setting]):
            self.setting_service.register_settings(settings)

    settings = app_commands.Group(
            name="setting",
            description="Various settings",
            guild_only=True
    )

    @settings.command(name="set")
    @app_commands.describe(
            setting="Setting name",
            value="Setting value"
    )
    async def settings_set(
            self,
            ctx: Interaction,
            setting: Transform[str, SettingNameTransformer],
            value: Transform[str, SettingValueTransformer],
    ):
        """Set setting value"""
        abstract_setting = self.setting_service.set(ctx.guild_id, setting, value)
        setting_value = self.setting_service.get_value(ctx.guild_id, setting)

        await ctx.response.send_message(f"{abstract_setting.name_human} is now set to: {setting_value}", ephemeral=True)
