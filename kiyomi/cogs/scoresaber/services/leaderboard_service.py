import logging
from typing import Optional

import pyscoresaber
from pyscoresaber import NotFoundException

from ..storage import StorageUnitOfWork
from ..storage.model.leaderboard import Leaderboard
from ..storage.repository.leaderboard_repository import LeaderboardRepository
from kiyomi import BaseService, Kiyomi

_logger = logging.getLogger(__name__)


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
            try:
                leaderboard = await self.scoresaber.leaderboard_info_by_hash(song_hash, song_difficulty, song_game_mode)

                if not await self.storage_uow.leaderboards.exists(leaderboard.id):
                    return await self.repository.add(Leaderboard(leaderboard))
            except NotFoundException as e:
                _logger.warning("ScoreSaber", f"Could not find leaderboard with parameters: {song_hash=}, {song_game_mode=}, {song_difficulty=}")
                return

        return leaderboard

    async def get_by_id(
            self,
            leaderboard_id: int
    ) -> Optional[Leaderboard]:
        leaderboard = await self.repository.get_by_id(leaderboard_id)

        if not leaderboard:
            try:
                leaderboard = await self.scoresaber.leaderboard_info_by_id(leaderboard_id)

                if not await self.storage_uow.leaderboards.exists(leaderboard.id):
                    return await self.repository.add(Leaderboard(leaderboard))
            except NotFoundException as e:
                _logger.warning("ScoreSaber", f"Could not find leaderboard with parameters: {leaderboard_id=}")
                return

        return leaderboard
