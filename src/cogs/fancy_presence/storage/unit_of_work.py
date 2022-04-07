from src.cogs.fancy_presence.storage.repository.presence_repository import PresenceRepository
from src.kiyomi import BaseUnitOfWork
from src.kiyomi.database.database import Session


class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session: Session):
        super().__init__(session)

        self.presences = PresenceRepository()
