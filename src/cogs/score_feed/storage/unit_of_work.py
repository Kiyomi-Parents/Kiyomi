from sqlalchemy.ext.asyncio import AsyncSession

from src.kiyomi.database import BaseUnitOfWork
from .repository.sent_score_repository import SentScoreRepository


class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.sent_score_repo = SentScoreRepository(session)
