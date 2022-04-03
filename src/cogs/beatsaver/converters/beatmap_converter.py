import pybeatsaver
from discord.ext import commands

from src.cogs.beatsaver import BeatSaverAPI
from src.cogs.beatsaver.errors import SongNotFound
from src.kiyomi.errors import BadArgument


class BeatmapConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> pybeatsaver.ECharacteristic:
        beatsaver = ctx.bot.get_cog_api(BeatSaverAPI)

        try:
            return await beatsaver.beatmap_service.get_beatmap_by_key(argument)
        except SongNotFound:
            pass

        raise BadArgument(ctx, argument)
