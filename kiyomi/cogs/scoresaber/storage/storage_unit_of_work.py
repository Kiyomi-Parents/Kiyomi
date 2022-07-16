from sqlalchemy.ext.asyncio import AsyncSession

from .repository.guild_player_repository import GuildPlayerRepository
from .repository.leaderboard_repository import LeaderboardRepository
from .repository.player_repository import PlayerRepository
from .repository.score_repository import ScoreRepository
from kiyomi.database import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.players = PlayerRepository(self._session)
        self.scores = ScoreRepository(self._session)
        self.guild_players = GuildPlayerRepository(self._session)
        self.leaderboards = LeaderboardRepository(self._session)
