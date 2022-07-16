from typing import Optional

import pyscoresaber

from ..storage import StorageUnitOfWork
from ..storage.model.leaderboard import Leaderboard
from ..storage.repository.leaderboard_repository import LeaderboardRepository
from kiyomi import BaseService


class LeaderboardService(BaseService[Leaderboard, LeaderboardRepository, StorageUnitOfWork]):
    async def get_by_song_hash(
            self,
            song_hash: str,
            song_game_mode: pyscoresaber.GameMode,
            song_difficulty: pyscoresaber.BeatmapDifficulty,
    ) -> Optional[Leaderboard]:
        return await self.repository.get_by_song_hash(song_hash, song_game_mode, song_difficulty)
