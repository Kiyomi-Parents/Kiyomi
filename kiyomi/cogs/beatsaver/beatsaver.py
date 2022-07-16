import logging
from typing import List, TYPE_CHECKING

from discord import app_commands, Interaction
from discord.app_commands import Transform
from discord.ext import commands

from kiyomi.cogs.settings.storage.model.emoji_setting import EmojiSetting
from kiyomi import BaseCog
from .services import ServiceUnitOfWork
from .errors import BeatmapNotFound
from .messages.views.song_view import SongView
from .storage.model.beatmap import Beatmap
from .transformers.beatmap_key_transformer import BeatmapKeyTransformer

if TYPE_CHECKING:
    from kiyomi.cogs.scoresaber.storage.model.leaderboard import Leaderboard

_logger = logging.getLogger(__name__)


class BeatSaver(BaseCog[ServiceUnitOfWork], name="Beat Saver"):
    def register_events(self):
        @self.bot.events.on("on_new_leaderboards")
        async def attach_song_to_score(leaderboards: List["Leaderboard"]):
            song_hashes = [leaderboard.song_hash for leaderboard in leaderboards]

            try:
                await self.service_uow.beatmaps.get_beatmaps_by_hashes(list(set(song_hashes)))
                await self.service_uow.save_changes()

                _logger.info("Beatmap import", f"Imported {len(list(set(song_hashes)))} songs")
            except BeatmapNotFound as error:
                _logger.info("on_new_leaderboards", error)

            await self.service_uow.close()

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            EmojiSetting.create(self.bot, "Easy emoji", "easy_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Normal emoji", "normal_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Hard emoji", "hard_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Expert emoji", "expert_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Expert+ emoji", "expert_plus_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Standard emoji", "standard_game_mode_emoji"),
            EmojiSetting.create(self.bot, "One Saber emoji", "one_saber_game_mode_emoji"),
            EmojiSetting.create(self.bot, "No Arrows emoji", "no_arrows_game_mode_emoji"),
            EmojiSetting.create(self.bot, "90 Degree emoji", "90_degree_game_mode_emoji"),
            EmojiSetting.create(self.bot, "360 Degree emoji", "360_degree_game_mode_emoji"),
            EmojiSetting.create(self.bot, "Lightshow emoji", "lightshow_game_mode_emoji"),
            EmojiSetting.create(self.bot, "Lawless emoji", "lawless_game_mode_emoji"),
            EmojiSetting.create(self.bot, "Map preview emoji", "map_preview_emoji"),
        ]

        self.bot.events.emit("setting_register", settings)

    @app_commands.command()
    @app_commands.rename(beatmap="key")
    @app_commands.describe(beatmap="Beatmap key (25f)")
    async def map(self, ctx: Interaction, beatmap: Transform[Beatmap, BeatmapKeyTransformer]):
        """Displays song info."""

        song_view = SongView(self.bot, ctx.guild, beatmap)

        await song_view.respond(ctx)
