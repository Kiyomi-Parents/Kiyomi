from sqlalchemy.orm import Session

from .repository.guild_player_repository import GuildPlayerRepository
from .repository.leaderboard_repository import LeaderboardRepository
from .repository.player_repository import PlayerRepository
from .repository.score_repository import ScoreRepository
from src.kiyomi.database import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)

        self.players = PlayerRepository(session)
        self.scores = ScoreRepository(session)
        self.guild_players = GuildPlayerRepository(session)
        self.leaderboards = LeaderboardRepository(session)
