from typing import Optional

import pybeatsaver
from discord import Guild

from src.cogs.beatsaver import BeatSaverUI, BeatSaverAPI
from src.cogs.beatsaver.storage.model.beatmap import Beatmap
from src.cogs.view_persistence.storage.model.persistence import Persistence
from src.cogs.view_persistence.storage.model.persistent_view import PersistentView
from src.kiyomi import Kiyomi
from ..components.buttons.guild_leaderboard_button import GuildLeaderboardButton


class GuildLeaderboardView(PersistentView):
    def __init__(
            self,
            bot: Kiyomi,
            guild: Guild,
            beatmap: Beatmap,
            characteristic: Optional[pybeatsaver.EDifficulty] = None,
            difficulty: Optional[pybeatsaver.ECharacteristic] = None
    ):
        self.beatmap = beatmap

        self._beatmap_characteristic: Optional[pybeatsaver.ECharacteristic] = characteristic
        self._beatmap_difficulty: Optional[pybeatsaver.EDifficulty] = difficulty

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
        beatsaver_ui = self.bot.get_cog_api(BeatSaverUI)

        self.add_item(beatsaver_ui.select_map_detail_characteristic(self.bot, self, self.beatmap))
        self.add_item(beatsaver_ui.select_map_detail_difficulty(self.bot, self, self.beatmap))

        self.add_item(GuildLeaderboardButton(self.bot, self, self.beatmap.latest_version.hash))

    async def serialize_persistence(self) -> Persistence:
        return Persistence(
                self.guild.id,
                self.message.channel.id,
                self.message.id,
                GuildLeaderboardView.__name__,
                self.beatmap.id,
                self._beatmap_characteristic.serialize if self._beatmap_characteristic is not None else None,
                self._beatmap_difficulty.serialize if self._beatmap_difficulty is not None else None
        )

    @staticmethod
    async def deserialize_persistence(bot: Kiyomi, persistence: Persistence) -> PersistentView:
        guild = bot.get_guild(persistence.guild_id)
        beatsaver = bot.get_cog_api(BeatSaverAPI)
        beatmap = await beatsaver.get_beatmap_by_key(persistence.get_param(0))

        characteristic = pybeatsaver.ECharacteristic.deserialize(persistence.get_param(1))
        difficulty = pybeatsaver.EDifficulty.deserialize(persistence.get_param(2))

        return GuildLeaderboardView(bot, guild, beatmap, characteristic, difficulty)
