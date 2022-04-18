import pybeatsaver
from discord.ext import commands
from discord.ext.commands import Context

from src.kiyomi.error import BadArgument


class BeatmapDifficultyConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str) -> pybeatsaver.EDifficulty:
        if pybeatsaver.EDifficulty.has_value(argument):
            return pybeatsaver.EDifficulty.deserialize(argument)

        raise BadArgument(ctx, argument)
