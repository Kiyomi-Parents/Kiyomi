from typing import Optional

import pybeatsaver
from discord import Guild

from ...scoresaber_api import ScoreSaberAPI
from ..components.buttons.score_button import ScoreButton
from ...scoresaber_utils import ScoreSaberUtils
from ...storage.model.score import Score
from src.cogs.view_persistence.storage.model.persistence import Persistence
from src.cogs.view_persistence.storage.model.persistent_view import PersistentView
from src.kiyomi import Kiyomi


class ScoreView(PersistentView):
    def __init__(self, bot: Kiyomi, guild: Guild, score: Score, previous_score: Optional[Score]):
        self.score = score
        self.previous_score = previous_score

        super().__init__(bot, guild)

    @property
    def beatmap_difficulty(self) -> Optional[pybeatsaver.EDifficulty]:
        return ScoreSaberUtils.to_beatsaver_difficulty(self.score.leaderboard.difficulty)

    @property
    def beatmap_characteristic(self) -> Optional[pybeatsaver.ECharacteristic]:
        return ScoreSaberUtils.to_beatsaver_characteristic(self.score.leaderboard.game_mode)

    def update_buttons(self):
        self.add_item(ScoreButton(self.bot, self, self.score, self.previous_score))

        if self.score.leaderboard is not None:
            leaderboard_ui = self.bot.get_cog("LeaderboardUI")
            self.add_item(leaderboard_ui.button_guild_leaderboard(self.bot, self, self.score.leaderboard.song_hash))

        if self.score.beatmap is not None:
            beatsaver_ui = self.bot.get_cog("BeatSaverUI")
            self.add_item(beatsaver_ui.button_beat_saver(self.bot, self, self.score.beatmap.id))
            self.add_item(beatsaver_ui.button_map_preview(self.bot, self, self.score.beatmap))

    async def serialize_persistence(self) -> Persistence:
        if self.previous_score is not None:
            return Persistence(
                self.guild.id,
                self.message.channel.id,
                self.message.id,
                ScoreView.__name__,
                str(self.score.id),
                str(self.previous_score.id),
            )

        return Persistence(
            self.guild.id,
            self.message.channel.id,
            self.message.id,
            ScoreView.__name__,
            str(self.score.id),
        )

    @staticmethod
    async def deserialize_persistence(bot: Kiyomi, persistence: Persistence):
        guild = bot.get_guild(persistence.guild_id)
        scoresaber = bot.get_cog_api(ScoreSaberAPI)
        score = scoresaber.get_score_by_id(int(persistence.get_param(0)))
        previous_score = None

        previous_score_id = persistence.get_param(1)
        if previous_score_id is not None:
            previous_score = scoresaber.get_score_by_id(int(previous_score_id))

        return ScoreView(bot, guild, score, previous_score)
