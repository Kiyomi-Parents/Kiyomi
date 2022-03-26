from typing import List

import discord
from discord import slash_command
from discord.ext import commands

from src.kiyomi import Kiyomi
from src.log import Logger
from .beatsaver_cog import BeatSaverCog
from .errors import SongNotFound
from .messages.views.song_view import SongView
from .services import BeatmapService
from src.cogs.settings.storage.model.emoji_setting import EmojiSetting
from src.cogs.scoresaber.storage.model.leaderboard import Leaderboard


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
            EmojiSetting.create(self.bot, "expert_plus_difficulty_emoji", None),
            EmojiSetting.create(self.bot, "standard_game_mode_emoji", None),
            EmojiSetting.create(self.bot, "one_saber_game_mode_emoji", None),
            EmojiSetting.create(self.bot, "no_arrows_game_mode_emoji", None),
            EmojiSetting.create(self.bot, "90_degree_game_mode_emoji", None),
            EmojiSetting.create(self.bot, "360_degree_game_mode_emoji", None),
            EmojiSetting.create(self.bot, "lightshow_game_mode_emoji", None),
            EmojiSetting.create(self.bot, "lawless_game_mode_emoji", None)
        ]

        self.bot.events.emit("setting_register", settings)

    @slash_command(aliases=["bsr", "song"])
    async def map(self, ctx: discord.ApplicationContext, key: str):
        """Displays song info."""
        try:
            db_beatmap = await self.beatmap_service.get_beatmap_by_key(key)
            song_view = SongView(self.bot, ctx.interaction.guild, db_beatmap)

            await song_view.respond(ctx.interaction)
        except SongNotFound as error:
            await ctx.respond(error)
