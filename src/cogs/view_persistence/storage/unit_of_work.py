from sqlalchemy.orm import Session

from .repository.message_view_repository import MessageViewRepository
from src.kiyomi import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session: Session):
        super().__init__(session)

        self.message_views = MessageViewRepository(self.session)
