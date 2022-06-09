from typing import List

import pybeatsaver

from src.kiyomi import Kiyomi
from .leaderboard_cog import LeaderboardCog
from .services import PlayerLeaderboardService, ScoreLeaderboardService
from .storage import UnitOfWork
from src.cogs.scoresaber.storage.model.score import Score


class LeaderboardAPI(LeaderboardCog):
    def __init__(
        self,
        bot: Kiyomi,
        player_leaderboard_service: PlayerLeaderboardService,
        score_leaderboard_service: ScoreLeaderboardService,
        uow: UnitOfWork,
    ):
        super().__init__(bot, player_leaderboard_service, score_leaderboard_service)

        self.uow = uow

    async def get_score_leaderboard(
        self,
        guild_id: int,
        beatmap_hash: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> List[Score]:
        return await self.score_leaderboard_service.get_beatmap_score_leaderboard(
            guild_id, beatmap_hash, characteristic, difficulty
        )

    async def get_player_top_scores_leaderboard(self, player_id: str) -> List[Score]:
        return await self.score_leaderboard_service.get_player_top_scores_leaderboard(player_id)
