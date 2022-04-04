from discord.ext import commands

from ..settings_api import SettingsAPI
from src.kiyomi.base_converter import BaseConverter


class SettingNameConverter(BaseConverter):
    async def convert(self, ctx: commands.Context, argument: str) -> str:
        settings = ctx.bot.get_cog_api(SettingsAPI)

        settings.get(ctx.guild.id, argument)
        return argument
