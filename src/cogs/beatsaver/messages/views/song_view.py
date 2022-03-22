import discord
import pybeatsaver
from discord import Embed
from discord.ui import Button
from pyee import AsyncIOEventEmitter

from src.cogs.beatsaver.messages.components.buttons.guild_leaderboard_button import GuildLeaderboardButton
from src.cogs.beatsaver.messages.components.buttons.map_details_button import MapDetailsButton
from src.cogs.beatsaver.messages.components.buttons.map_preview_button import MapPreviewButton
from src.cogs.beatsaver.messages.components.selects.map_detail_difficulty_select import MapDetailDifficultySelect
from src.cogs.beatsaver.storage import Beatmap
from src.cogs.leaderboard import LeaderboardAPI
from src.kiyomi import Kiyomi

from src.kiyomi.base_view import BaseView


class SongView(BaseView):

    events = AsyncIOEventEmitter()

    def __init__(self, bot: Kiyomi, beatmap: Beatmap):
        super().__init__(bot)

        self.bot = bot
        self.beatmap = beatmap

        self.add_item(MapDetailsButton(bot, beatmap, self.events))
        self.add_item(GuildLeaderboardButton(bot, beatmap.id))
        self.add_item(MapPreviewButton(bot, beatmap.id))
        self.add_item(MapDetailDifficultySelect(bot, beatmap, self.events, self._get_embed_update_funcs()))

    def _get_embed_update_funcs(self):
        result = []
        for component in self.children:
            update_embed_func = getattr(component, "update_embed", None)
            if update_embed_func is not None and callable(update_embed_func):
                result.append(update_embed_func)
        return result
