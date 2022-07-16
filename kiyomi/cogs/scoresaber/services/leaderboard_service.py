from typing import Optional

import pyscoresaber

from ..storage import StorageUnitOfWork
from ..storage.model.leaderboard import Leaderboard
from ..storage.repository.leaderboard_repository import LeaderboardRepository
from kiyomi import BaseService, Kiyomi


class LeaderboardService(BaseService[Leaderboard, LeaderboardRepository, StorageUnitOfWork]):
    def __init__(
        self,
        bot: Kiyomi,
        repository: LeaderboardRepository,
        storage_uow: StorageUnitOfWork,
        scoresaber: pyscoresaber.ScoreSaberAPI,
    ):
        super().__init__(bot, repository, storage_uow)

        self.scoresaber = scoresaber

    async def get_by_song_hash(
            self,
            song_hash: str,
            song_game_mode: pyscoresaber.GameMode,
            song_difficulty: pyscoresaber.BeatmapDifficulty,
    ) -> Optional[Leaderboard]:
        leaderboard = await self.repository.get_by_song_hash(song_hash, song_game_mode, song_difficulty)

        if not leaderboard:
            leaderboard = await self.scoresaber.leaderboard_info_by_hash(song_hash, song_difficulty, song_game_mode)
            
            if not await self.storage_uow.leaderboards.exists(leaderboard.id):
                return await self.repository.add(Leaderboard(leaderboard))
