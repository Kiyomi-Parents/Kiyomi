from typing import List

import discord
from discord import slash_command
from discord.ext import commands

from .messages.views.song_view import SongView
from .services import BeatmapService
from .beatsaver_cog import BeatSaverCog
from .errors import SongNotFound
from src.log import Logger
from src.kiyomi import Kiyomi
from src.cogs.leaderboard import LeaderboardAPI
from src.cogs.settings import SettingsAPI
from src.cogs.scoresaber.storage import Leaderboard
from src.cogs.settings.storage.model.emoji_setting import EmojiSetting


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

        settings = [
            EmojiSetting.create(self.bot, "easy_difficulty_emoji", None),
            EmojiSetting.create(self.bot, "normal_difficulty_emoji", None),
            EmojiSetting.create(self.bot, "hard_difficulty_emoji", None),
            EmojiSetting.create(self.bot, "expert_difficulty_emoji", None),
            EmojiSetting.create(self.bot, "expert_plus_difficulty_emoji", None)
        ]

        self.bot.events.emit("setting_register", settings)

    # 22fcf
    @slash_command(aliases=["bsr", "song"], guild_ids=[198040147189694464])
    async def map(self, ctx: discord.ApplicationContext, key: str):
        """Displays song info."""
        leaderboard = self.bot.get_cog_api(LeaderboardAPI)
        settings = self.bot.get_cog_api(SettingsAPI)

        try:
            db_beatmap = await self.beatmap_service.get_beatmap_by_key(key)

            song_view = SongView(self.bot, ctx.interaction.guild, db_beatmap)

            await song_view.respond(ctx.interaction)

            # TODO: Remove this probably
            if settings.get(ctx.guild.id, "map_leaderboard"):
                leaderboard_embed = await leaderboard.get_player_score_leaderboard_embed(ctx.guild.id, key)

                await ctx.respond(embed=leaderboard_embed)
        except SongNotFound as error:
            await ctx.respond(error)
