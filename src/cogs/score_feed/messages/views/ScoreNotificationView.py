from typing import Optional

from discord import Guild

from src.cogs.beatsaver.storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty
from src.cogs.scoresaber import ScoreSaberAPI
from ..components.buttons.beatsaver_button import BeatSaverButton
from ..components.buttons.score_button import ScoreButton
from src.cogs.scoresaber.storage.model.score import Score
from src.cogs.view_persistence.storage.model.persistence import Persistence
from src.cogs.view_persistence.storage.model.persistent_view import PersistentView
from src.kiyomi import Kiyomi


class ScoreNotificationView(PersistentView):

    def __init__(self, bot: Kiyomi, guild: Guild, score: Score, previous_score: Optional[Score]):
        self.score = score
        self.previous_score = previous_score

        super().__init__(bot, guild)

    @property
    def beatmap_version_difficulty(self) -> Optional[BeatmapVersionDifficulty]:
        return self.score.beatmap_difficulty

    def update_buttons(self):
        self.add_item(ScoreButton(self.bot, self, self.score, self.previous_score))

        leaderboard = self.bot.get_cog("LeaderboardAPI")
        guild_leaderboard_button = leaderboard.get_guild_leaderboard_button(
                self.bot,
                self,
                self.score.leaderboard.song_hash
        )
        self.add_item(guild_leaderboard_button)

        if self.score.beatmap is not None:
            self.add_item(BeatSaverButton(self.bot, self, self.score.beatmap.id))

    async def serialize_persistence(self) -> Persistence:
        if self.previous_score is not None:
            return Persistence(self.guild.id, self.message.channel.id, self.message.id, ScoreNotificationView.__name__, str(self.score.id), str(self.previous_score.id))

        return Persistence(self.guild.id, self.message.channel.id, self.message.id, ScoreNotificationView.__name__, str(self.score.id))

    @staticmethod
    async def deserialize_persistence(bot: Kiyomi, persistence: Persistence):
        guild = bot.get_guild(persistence.guild_id)
        scoresaber = bot.get_cog_api(ScoreSaberAPI)
        score = scoresaber.get_score_by_id(persistence.view_parameters[0])
        previous_score = None

        if len(persistence.view_parameters) > 1:
            previous_score_id = persistence.view_parameters[1]
            if previous_score_id is not None:
                previous_score = scoresaber.get_score_by_id(previous_score_id)

        return ScoreNotificationView(bot, guild, score, previous_score)
