from typing import List

import pybeatsaver

from kiyomi.cogs.scoresaber.storage.model.score import Score
from kiyomi import BaseCog
from .services import ServiceUnitOfWork


class LeaderboardAPI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    async def get_score_leaderboard(
        self,
        guild_id: int,
        beatmap_hash: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> List[Score]:
        return await self.service_uow.score_leaderboards.get_beatmap_score_leaderboard(
            guild_id, beatmap_hash, characteristic, difficulty
        )

    async def get_player_top_scores_leaderboard(self, player_id: str) -> List[Score]:
        return await self.service_uow.score_leaderboards.get_player_top_scores_leaderboard(player_id)
