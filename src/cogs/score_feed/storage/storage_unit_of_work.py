from sqlalchemy.ext.asyncio import AsyncSession

from src.kiyomi.database import BaseStorageUnitOfWork
from .repository.sent_score_repository import SentScoreRepository


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.sent_scores = SentScoreRepository(self._session)
