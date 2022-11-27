import logging
from typing import List, TYPE_CHECKING, Optional

import discord
from discord import app_commands, Interaction, Permissions
from discord.app_commands import Transform
from discord.ext import commands

from kiyomi.cogs.settings.storage.model.emoji_setting import EmojiSetting
from kiyomi import BaseCog
from .services import ServiceUnitOfWork
from .errors import BeatmapNotFound
from .messages.views.song_view import SongView
from .storage.model.beatmap import Beatmap
from .transformers.beatmap_key_transformer import BeatmapKeyTransformer
from ..settings import SettingsAPI
from ..settings.storage.model.toggle_setting import ToggleSetting

if TYPE_CHECKING:
    from kiyomi.cogs.scoresaber.storage.model.leaderboard import Leaderboard

_logger = logging.getLogger(__name__)


class BeatSaver(BaseCog[ServiceUnitOfWork], name="Beat Saver"):
    def register_events(self):
        @self.bot.events.on("on_new_leaderboards")
        async def attach_song_to_score(leaderboards: List["Leaderboard"]):
            song_hashes = [leaderboard.song_hash for leaderboard in leaderboards]

            try:
                await self._service_uow.beatmaps.get_beatmaps_by_hashes(list(set(song_hashes)))
                await self._service_uow.save_changes()

                _logger.info("Beatmap import", f"Imported {len(list(set(song_hashes)))} songs")
            except BeatmapNotFound as error:
                _logger.info("on_new_leaderboards", error)

            await self._service_uow.close()

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            EmojiSetting.create(self.bot, self.__cog_name__, "Easy emoji", "easy_difficulty_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "Normal emoji", "normal_difficulty_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "Hard emoji", "hard_difficulty_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "Expert emoji", "expert_difficulty_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "Expert+ emoji", "expert_plus_difficulty_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "Standard emoji", "standard_game_mode_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "One Saber emoji", "one_saber_game_mode_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "No Arrows emoji", "no_arrows_game_mode_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "90 Degree emoji", "90_degree_game_mode_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "360 Degree emoji", "360_degree_game_mode_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "Lightshow emoji", "lightshow_game_mode_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "Lawless emoji", "lawless_game_mode_emoji"),
            EmojiSetting.create(self.bot, self.__cog_name__, "Map preview emoji", "map_preview_emoji"),
            ToggleSetting.create(self.__cog_name__, "Reply to beatmap links with a nice beatmap embed", "text_to_beatmap", permissions=Permissions(administrator=True), default_value=True)
        ]

        self.bot.events.emit("setting_register", settings)

    @app_commands.command()
    @app_commands.rename(beatmap="key")
    @app_commands.describe(beatmap="Beatmap key (25f)")
    async def map(self, ctx: Interaction, beatmap: Transform[Optional[Beatmap], BeatmapKeyTransformer]):
        """Displays song info."""
        await ctx.response.defer()

        song_view = SongView(self.bot, ctx.guild, beatmap)

        await song_view.respond(ctx)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """Repost emoji if enabled"""

        if msg.guild is None:
            return

        if msg.author.id == self.bot.user.id:
            return

        async with self.bot.get_cog_api(SettingsAPI) as settings:
            text_to_beatmap_enabled = await settings.get(msg.guild.id, "text_to_beatmap")

        if text_to_beatmap_enabled:
            beatmap = await self._service_uow.beatmaps_from_text.get_beatmap_from_text(msg.content)

            await self._service_uow.save_changes()
            await self._service_uow.refresh(beatmap)

            if beatmap is not None:
                song_view = SongView(self.bot, msg.guild, beatmap)
                await song_view.reply(msg)

        await self._service_uow.close()
