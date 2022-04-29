from typing import List

from discord import app_commands, Interaction
from discord.app_commands import Choice

from src.kiyomi import Kiyomi, Utils
from .errors import PermissionDenied
from .services import SettingService
from .services.settings_autocomplete_service import SettingAutocompleteService
from .settings_cog import SettingsCog
from .storage import Setting


class Settings(SettingsCog):

    def __init__(
            self,
            bot: Kiyomi,
            setting_service: SettingService,
            settings_autocomplete_service: SettingAutocompleteService
    ):
        super().__init__(bot, setting_service, settings_autocomplete_service)

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
    @app_commands.describe(setting="Setting name", value="Setting value")
    async def settings_set(
            self,
            ctx: Interaction,
            setting: str,
            value: str
    ):
        """Set setting value"""

        if not self.setting_service.has_permission(setting, ctx.user):
            raise PermissionDenied(setting)

        await self.setting_service.validate_setting_value(ctx.guild_id, setting, value)

        abstract_setting = self.setting_service.set(ctx.guild_id, setting, value)
        setting_value = self.setting_service.get_value(ctx.guild_id, setting)

        await ctx.response.send_message(f"{abstract_setting.name_human} is now set to: {setting_value}", ephemeral=True)

    # Workaround
    @settings_set.autocomplete("setting")
    async def settings_autocomplete(self, ctx: Interaction, current: str) -> List[Choice[str]]:
        choices = self.settings_autocomplete_service.get_settings(ctx, current)

        return Utils.limit_list(choices, 25)

    @settings_set.autocomplete("value")
    async def get_setting_values(self, ctx: Interaction, current: str) -> List[Choice[str]]:
        choices = await self.settings_autocomplete_service.get_setting_values(ctx, current)

        return Utils.limit_list(choices, 25)
