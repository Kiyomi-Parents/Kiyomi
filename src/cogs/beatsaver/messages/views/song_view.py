from typing import Optional

import pybeatsaver
from discord import Guild

from src.cogs.view_persistence.storage.model.persistence import Persistence
from src.cogs.view_persistence.storage.model.persistent_view import PersistentView
from src.kiyomi import Kiyomi
from src.kiyomi.base_view import BaseView
from ...beatsaver_api import BeatSaverAPI
from ...storage.model.beatmap import Beatmap
from ..components.buttons.map_details_button import MapDetailsButton
from ..components.buttons.map_preview_button import MapPreviewButton
from ..components.selects.map_detail_characteristic_select import MapDetailCharacteristicSelect
from ..components.selects.map_detail_difficulty_select import MapDetailDifficultySelect


# Add NPS graph button
class SongView(PersistentView):

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

    def update_buttons(self):
        self.add_item(MapDetailCharacteristicSelect(self.bot, self, self.beatmap))
        self.add_item(MapDetailDifficultySelect(self.bot, self, self.beatmap))

        self.add_item(MapDetailsButton(self.bot, self, self.beatmap))

        leaderboard_ui = self.bot.get_cog("LeaderboardUI")
        self.add_item(leaderboard_ui.button_guild_leaderboard(
                self.bot,
                self,
                self.beatmap.latest_version.hash
        ))

        self.add_item(MapPreviewButton(self.bot, self, self.beatmap))

    async def serialize_persistence(self) -> Persistence:
        return Persistence(self.guild.id, self.message.channel.id, self.message.id, SongView.__name__, self.beatmap.id)

    @staticmethod
    async def deserialize_persistence(bot: Kiyomi, persistence: Persistence) -> BaseView:
        guild = bot.get_guild(persistence.guild_id)
        beatsaver = bot.get_cog_api(BeatSaverAPI)
        beatmap = await beatsaver.get_beatmap_by_key(persistence.view_parameters[0])

        return SongView(bot, guild, beatmap)
