from pyee import AsyncIOEventEmitter

from src.cogs.beatsaver.messages.components.buttons.guild_leaderboard_button import GuildLeaderboardButton
from src.cogs.beatsaver.messages.components.buttons.map_details_button import MapDetailsButton
from src.cogs.beatsaver.messages.components.buttons.map_preview_button import MapPreviewButton
from src.cogs.beatsaver.messages.components.selects.map_detail_difficulty_select import MapDetailDifficultySelect
from src.cogs.beatsaver.storage import Beatmap
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
        self.add_item(MapPreviewButton(bot, beatmap))
        self.add_item(MapDetailDifficultySelect(bot, beatmap, self.events, self.update_funcs))

    @property
    def update_funcs(self):
        result = []
        for component in self.children:
            update_func = getattr(component, "update", None)
            if update_func is not None and callable(update_func):
                result.append(update_func)
        return result
