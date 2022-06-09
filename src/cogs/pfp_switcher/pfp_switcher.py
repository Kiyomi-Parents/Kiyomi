from .services import ServiceUnitOfWork
from src.kiyomi import BaseCog


class PFPSwitcher(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass
