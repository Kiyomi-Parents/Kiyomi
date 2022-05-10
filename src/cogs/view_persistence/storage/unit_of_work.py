from sqlalchemy.ext.asyncio import AsyncSession

from .repository.message_view_repository import MessageViewRepository
from src.kiyomi import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.message_views = MessageViewRepository(session)
