from .repository.message_view_repository import MessageViewRepository
from src.kiyomi import BaseUnitOfWork
from src.kiyomi.database.database import Session


class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session: Session):
        super().__init__(session)

        self.message_views = MessageViewRepository(self.session)
