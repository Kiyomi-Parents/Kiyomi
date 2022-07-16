from pyscoresaber import ScoreSaberAPI

from .guild_player_service import GuildPlayerService
from .leaderboard_service import LeaderboardService
from .player_service import PlayerService
from ..storage import StorageUnitOfWork
from kiyomi import BaseServiceUnitOfWork, Kiyomi
from .score_service import ScoreService


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork, scoresaber: ScoreSaberAPI):
        super().__init__(storage_uow)

        self.players = PlayerService(bot, storage_uow.players, storage_uow, scoresaber)
        self.scores = ScoreService(bot, storage_uow.scores, storage_uow, scoresaber)
        self.guild_players = GuildPlayerService(bot, storage_uow.guild_players, storage_uow)
        self.leaderboards = LeaderboardService(bot, storage_uow.leaderboards, storage_uow)
