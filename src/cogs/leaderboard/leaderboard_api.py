from typing import List

from src.kiyomi import Kiyomi
from .leaderboard_cog import LeaderboardCog
from .messages.components.buttons.guild_leaderboard_button import GuildLeaderboardButton
from .services import PlayerLeaderboardService, ScoreLeaderboardService
from .storage import UnitOfWork
from src.cogs.scoresaber.storage.model.score import Score
from ..beatsaver.storage.model.beatmap import Beatmap
from ..beatsaver.storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty
from src.kiyomi.base_view import BaseView


class LeaderboardAPI(LeaderboardCog):
    def __init__(self, bot: Kiyomi, player_leaderboard_service: PlayerLeaderboardService, score_leaderboard_service: ScoreLeaderboardService, uow: UnitOfWork):
        super().__init__(bot, player_leaderboard_service, score_leaderboard_service)

        self.uow = uow

    async def get_score_leaderboard(self, guild_id: int, beatmap_difficulty: BeatmapVersionDifficulty):
        return await self.score_leaderboard_service.get_beatmap_score_leaderboard(guild_id, beatmap_difficulty)

    @staticmethod
    def get_guild_leaderboard_button(bot: Kiyomi, parent: BaseView, beatmap: Beatmap) -> GuildLeaderboardButton:
        return GuildLeaderboardButton(bot, parent, beatmap)

    def get_player_top_scores_leaderboard(self, player_id: str) -> List[Score]:
        return self.score_leaderboard_service.get_player_top_scores_leaderboard(player_id)
