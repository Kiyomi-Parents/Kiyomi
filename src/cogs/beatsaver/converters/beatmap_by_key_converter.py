from discord.ext import commands

from ..beatsaver_api import BeatSaverAPI
from ..storage.model.beatmap import Beatmap


class BeatmapByKeyConverter(commands.Converter[Beatmap]):
    async def convert(self, ctx: commands.Context, argument: str) -> Beatmap:
        beatsaver = ctx.bot.get_cog_api(BeatSaverAPI)

        return await beatsaver.beatmap_service.get_beatmap_by_key(argument)
