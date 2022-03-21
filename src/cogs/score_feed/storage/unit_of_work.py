from sqlalchemy.orm import Session

from src.database import BaseUnitOfWork
from .repository.sent_score_repository import SentScoreRepository
from ...scoresaber.storage.repository.player_repository import PlayerRepository
from ...scoresaber.storage.repository.score_repository import ScoreRepository


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)

        self.sent_score_repo = SentScoreRepository(session)
        # self.score_repo = ScoreRepository(session)
        # self.player_repo = PlayerRepository(session)
