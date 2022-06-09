from ..storage import StorageUnitOfWork
from ..storage.model.leaderboard import Leaderboard
from ..storage.repository.leaderboard_repository import LeaderboardRepository
from src.kiyomi import BaseService


class LeaderboardService(BaseService[Leaderboard, LeaderboardRepository, StorageUnitOfWork]):
    pass
