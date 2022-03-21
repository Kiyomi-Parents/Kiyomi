from sqlalchemy.orm import Session

from .repository import PlayerRepository, ScoreRepository, LeaderboardRepository, \
    GuildPlayerRepository
from src.database.base_unit_of_work import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)

        self.players = PlayerRepository(session)
        self.scores = ScoreRepository(session)
        self.guild_players = GuildPlayerRepository(session)
        self.leaderboards = LeaderboardRepository(session)
