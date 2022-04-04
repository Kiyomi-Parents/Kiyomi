from typing import List

import discord
from discord import slash_command, Option, OptionChoice

from src.kiyomi import Kiyomi
from .leaderboard_cog import LeaderboardCog
from .messages.components.embeds.guild_leaderboard_embed import GuildLeaderboardEmbed
from .services import PlayerLeaderboardService, ScoreLeaderboardService
from ..beatsaver import BeatSaverAPI
from ..beatsaver.converters.beatmap_characteristic_converter import BeatmapCharacteristicConverter
from ..beatsaver.converters.beatmap_converter import BeatmapConverter
from ..beatsaver.converters.beatmap_difficulty_converter import BeatmapDifficultyConverter
from src.kiyomi.errors import BadArgument


class Leaderboard(LeaderboardCog):
    def __init__(self, bot: Kiyomi, player_leaderboard_service: PlayerLeaderboardService, score_leaderboard_service: ScoreLeaderboardService):
        super().__init__(bot, player_leaderboard_service, score_leaderboard_service)

        # Register events
        self.events()

    def events(self):
        pass

    async def get_beatmap_difficulties(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        beatsaver = self.bot.get_cog_api(BeatSaverAPI)

        try:
            beatmap = await BeatmapConverter().convert(ctx, ctx.options["key"])
            beatmap_characteristic = await BeatmapCharacteristicConverter().convert(ctx, ctx.options["game_mode"])
        except BadArgument:
            return []

        return await beatsaver.beatmap_autocomplete_service.get_beatmap_difficulties_by_key(beatmap, beatmap_characteristic)

    async def get_beatmap_characteristics(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        beatsaver = self.bot.get_cog_api(BeatSaverAPI)

        try:
            beatmap = await BeatmapConverter().convert(ctx, ctx.options["key"])
        except BadArgument:
            return []

        return await beatsaver.beatmap_autocomplete_service.get_beatmap_characteristics_by_key(beatmap)

    @slash_command()
    async def leaderboard(
        self,
        ctx: discord.ApplicationContext,
        key: Option(
                BeatmapConverter,
                "Beatmap key (!bsr 25f)"
        ),
        game_mode: Option(
                BeatmapCharacteristicConverter,
                "Beatmap game mode",
                autocomplete=get_beatmap_characteristics
        ),
        difficulty: Option(
                BeatmapDifficultyConverter,
                "Beatmap difficulty",
                autocomplete=get_beatmap_difficulties
        )
    ):
        """Displays songs guild leaderboard."""
        beatsaver = self.bot.get_cog_api(BeatSaverAPI)

        beatmap_difficulty = beatsaver.get_beatmap_difficulty_by_beatmap(key, game_mode, difficulty)
        leaderboard = await self.score_leaderboard_service.get_beatmap_score_leaderboard(ctx.guild.id, beatmap_difficulty)

        # TODO: Make this into a view with characteristic and difficulty selector
        guild_leaderboard_embed = GuildLeaderboardEmbed(self.bot, ctx.guild.name, beatmap_difficulty, leaderboard)
        await ctx.respond(embed=guild_leaderboard_embed)
