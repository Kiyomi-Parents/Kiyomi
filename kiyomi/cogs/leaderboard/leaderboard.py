from typing import Optional

import pybeatsaver
from discord import app_commands, Interaction
from discord.app_commands import Transform
from discord.ext import commands

from .services import ServiceUnitOfWork
from .messages.views.guild_leaderboard_view import GuildLeaderboardView
from ..beatsaver.storage.model.beatmap import Beatmap
from ..beatsaver.transformers.beatmap_characteristic_transformer import (
    BeatmapCharacteristicTransformer,
)
from ..beatsaver.transformers.beatmap_difficulty_transformer import (
    BeatmapDifficultyTransformer,
)
from ..beatsaver.transformers.beatmap_key_transformer import BeatmapKeyTransformer
from kiyomi import BaseCog
from ..settings.storage.model.emoji_setting import EmojiSetting


class Leaderboard(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            # TODO: Add bot owner permissions
            EmojiSetting.create(self.bot, self.__cog_name__, "Guild Leaderboard emoji", "guild_leaderboard_emoji"),
        ]

        self.bot.events.emit("setting_register", settings)

    @app_commands.command()
    @app_commands.rename(beatmap="key", characteristic="game_mode")
    @app_commands.describe(
        beatmap="Beatmap key (25f)",
        characteristic="Beatmap game mode",
        difficulty="Beatmap difficulty",
    )
    async def leaderboard(
        self,
        ctx: Interaction,
        beatmap: Transform[Beatmap, BeatmapKeyTransformer],
        characteristic: Optional[Transform[pybeatsaver.ECharacteristic, BeatmapCharacteristicTransformer]],
        difficulty: Optional[Transform[pybeatsaver.EDifficulty, BeatmapDifficultyTransformer]],
    ):
        """Displays songs guild leaderboard."""
        await ctx.response.defer()

        guild_leaderboard_view = GuildLeaderboardView(self.bot, ctx.guild, beatmap, characteristic, difficulty)

        await guild_leaderboard_view.respond(ctx)
