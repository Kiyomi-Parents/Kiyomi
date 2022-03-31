from typing import Optional

import pybeatsaver
from discord import Guild

from src.kiyomi import Kiyomi
from src.kiyomi.base_view import BaseView
from ...storage.model.beatmap import Beatmap
from ..components.buttons.map_details_button import MapDetailsButton
from ..components.buttons.map_preview_button import MapPreviewButton
from ..components.selects.map_detail_characteristic_select import MapDetailCharacteristicSelect
from ..components.selects.map_detail_difficulty_select import MapDetailDifficultySelect


# TODO:
# Need to save the view type and the message id to the database, for it to be truly persistent.
# When the bot restarts we need to attach all the attach all the views to the messages IDs in Kiyomi class (add_view)
# This could probably be a new cog?

# Add NPS graph button
from ...storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty


class SongView(BaseView):

    def __init__(self, bot: Kiyomi, guild: Guild, beatmap: Beatmap):
        self.beatmap = beatmap

        self._beatmap_difficulty: Optional[pybeatsaver.EDifficulty] = None
        self._beatmap_characteristic: Optional[pybeatsaver.ECharacteristic] = None

        super().__init__(bot, guild)

    @property
    def beatmap_difficulty(self) -> Optional[pybeatsaver.EDifficulty]:
        if self._beatmap_difficulty is None:
            return self.beatmap.latest_version.difficulties[-1].difficulty

        return self._beatmap_difficulty

    @beatmap_difficulty.setter
    def beatmap_difficulty(self, beatmap_difficulty: pybeatsaver.EDifficulty):
        self._beatmap_difficulty = beatmap_difficulty

    @property
    def beatmap_characteristic(self) -> Optional[pybeatsaver.ECharacteristic]:
        if self._beatmap_characteristic is None:
            return self.beatmap.latest_version.difficulties[-1].characteristic

        return self._beatmap_characteristic

    @beatmap_characteristic.setter
    def beatmap_characteristic(self, beatmap_characteristic: pybeatsaver.ECharacteristic):
        self._beatmap_characteristic = beatmap_characteristic

    @property
    def beatmap_version_difficulty(self) -> Optional[BeatmapVersionDifficulty]:
        for beatmap_difficulty in self.beatmap.latest_version.difficulties:
            if beatmap_difficulty.characteristic is not self.beatmap_characteristic:
                continue

            if beatmap_difficulty.difficulty is not self.beatmap_difficulty:
                continue

            return beatmap_difficulty

        return None

    def update_buttons(self):
        self.add_item(MapDetailCharacteristicSelect(self.bot, self, self.beatmap))
        self.add_item(MapDetailDifficultySelect(self.bot, self, self.beatmap))
        self.add_item(MapDetailsButton(self.bot, self, self.beatmap))

        leaderboard = self.bot.get_cog("LeaderboardAPI")
        guild_leaderboard_button = leaderboard.get_guild_leaderboard_button(self.bot, self, self.beatmap)
        self.add_item(guild_leaderboard_button)

        self.add_item(MapPreviewButton(self.bot, self, self.beatmap))
