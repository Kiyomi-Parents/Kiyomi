import pybeatsaver
from discord.ext import commands

from src.kiyomi.base_converter import BaseConverter
from src.kiyomi.error import BadArgument


class BeatmapCharacteristicConverter(BaseConverter):
    async def convert(self, ctx: commands.Context, argument: str) -> pybeatsaver.ECharacteristic:
        if pybeatsaver.ECharacteristic.has_value(argument):
            return pybeatsaver.ECharacteristic.deserialize(argument)

        raise BadArgument(ctx, argument)
