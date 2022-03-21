from typing import List

from discord import slash_command
from discord.ext import commands

from .services import BeatmapService
from .beatsaver_cog import BeatSaverCog
from .errors import SongNotFound
from .message import Message
from src.log import Logger
from src.kiyomi import Kiyomi
from src.cogs.leaderboard import LeaderboardAPI
from src.cogs.settings import SettingsAPI
from src.cogs.scoresaber.storage import Leaderboard


class BeatSaver(BeatSaverCog, name="Beat Saver"):
    def __init__(self, bot: Kiyomi, beatmap_service: BeatmapService):
        super().__init__(bot, beatmap_service)

        # Register events
        self.events()

    def events(self):

        @self.bot.events.on("on_new_leaderboards")
        async def attach_song_to_score(leaderboards: List[Leaderboard]):
            song_hashes = [leaderboard.song_hash for leaderboard in leaderboards]

            try:
                await self.beatmap_service.get_beatmaps_by_hashes(list(set(song_hashes)))
            except SongNotFound as error:
                Logger.log("on_new_leaderboards", error)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.beatmap_service.start_scoresaber_api_client()

    @slash_command(aliases=["bsr", "song"])
    async def map(self, ctx, key: str):
        """Displays song info."""
        leaderboard = self.bot.get_cog_api(LeaderboardAPI)
        settings = self.bot.get_cog_api(SettingsAPI)

        try:
            db_beatmap = await self.beatmap_service.get_beatmap_by_key(key)
            song_embed = Message.get_song_embed(db_beatmap)

            await ctx.respond(embed=song_embed)

            if settings.get(ctx.guild.id, "map_leaderboard"):
                leaderboard_embed = await leaderboard.get_player_score_leaderboard_embed(ctx.guild.id, key)

                await ctx.respond(embed=leaderboard_embed)
        except SongNotFound as error:
            await ctx.respond(error)
