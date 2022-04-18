from typing import List

import discord
from discord import slash_command, Option, OptionChoice

from src.kiyomi import Kiyomi
from .leaderboard_cog import LeaderboardCog
from .messages.views.guild_leaderboard_view import GuildLeaderboardView
from .services import PlayerLeaderboardService, ScoreLeaderboardService
from ..beatsaver import BeatSaverAPI
from ..beatsaver.converters.beatmap_characteristic_converter import BeatmapCharacteristicConverter
from ..beatsaver.converters.beatmap_by_key_converter import BeatmapByKeyConverter
from ..beatsaver.converters.beatmap_difficulty_converter import BeatmapDifficultyConverter
from src.kiyomi.error import BadArgument


class Leaderboard(LeaderboardCog):
    def __init__(
            self,
            bot: Kiyomi,
            player_leaderboard_service: PlayerLeaderboardService,
            score_leaderboard_service: ScoreLeaderboardService
    ):
        super().__init__(bot, player_leaderboard_service, score_leaderboard_service)

        # Register events
        self.events()

    def events(self):
        pass

    async def get_beatmap_difficulties(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        beatsaver = self.bot.get_cog_api(BeatSaverAPI)

        try:
            beatmap = await BeatmapByKeyConverter().convert(ctx, ctx.options["key"])
            beatmap_characteristic = await BeatmapCharacteristicConverter().convert(ctx, ctx.options["game_mode"])
        except BadArgument:
            return []

        return await beatsaver.beatmap_autocomplete_service.get_beatmap_difficulties_by_key(
                beatmap,
                beatmap_characteristic
        )

    async def get_beatmap_characteristics(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        beatsaver = self.bot.get_cog_api(BeatSaverAPI)

        try:
            beatmap = await BeatmapByKeyConverter().convert(ctx, ctx.options["key"])
        except BadArgument:
            return []

        return await beatsaver.beatmap_autocomplete_service.get_beatmap_characteristics_by_key(beatmap)

    @slash_command()
    async def leaderboard(
            self,
            ctx: discord.ApplicationContext,
            beatmap: Option(
                    BeatmapByKeyConverter,
                    name="key",
                    description="Beatmap key (25f)"
            ),
            characteristic: Option(
                    BeatmapCharacteristicConverter,
                    name="game_mode",
                    description="Beatmap game mode",
                    autocomplete=get_beatmap_characteristics
            ),
            difficulty: Option(
                    BeatmapDifficultyConverter,
                    description="Beatmap difficulty",
                    autocomplete=get_beatmap_difficulties
            )
    ):
        """Displays songs guild leaderboard."""
        guild_leaderboard_view = GuildLeaderboardView(self.bot, ctx.interaction.guild, beatmap, characteristic, difficulty)

        await guild_leaderboard_view.respond(ctx.interaction)
