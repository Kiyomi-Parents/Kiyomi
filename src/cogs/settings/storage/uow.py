from sqlalchemy.orm import Session

from src.kiyomi.database import BaseUnitOfWork
from .repository import SettingsRepository


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: Session):
        super().__init__(session)

        self.settings_repo = SettingsRepository(session)
