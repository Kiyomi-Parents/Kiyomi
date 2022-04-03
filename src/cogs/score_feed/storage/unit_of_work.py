from sqlalchemy.orm import Session

from src.kiyomi.database import BaseUnitOfWork
from .repository.sent_score_repository import SentScoreRepository


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)

        self.sent_score_repo = SentScoreRepository(session)
