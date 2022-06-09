from typing import Optional

import pybeatsaver
from discord import app_commands, Interaction
from discord.app_commands import Transform

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
from ...kiyomi import BaseCog


class Leaderboard(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

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
        guild_leaderboard_view = GuildLeaderboardView(self.bot, ctx.guild, beatmap, characteristic, difficulty)

        await guild_leaderboard_view.respond(ctx)
