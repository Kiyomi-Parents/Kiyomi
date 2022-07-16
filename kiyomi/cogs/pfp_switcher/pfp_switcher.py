from .services import ServiceUnitOfWork
from kiyomi import BaseCog


class PFPSwitcher(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass
