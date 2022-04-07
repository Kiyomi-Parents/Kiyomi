import pybeatsaver
from discord.ext import commands

from ..beatsaver_api import BeatSaverAPI


class BeatmapConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> pybeatsaver.ECharacteristic:
        beatsaver = ctx.bot.get_cog_api(BeatSaverAPI)

        return await beatsaver.beatmap_service.get_beatmap_by_key(argument)
