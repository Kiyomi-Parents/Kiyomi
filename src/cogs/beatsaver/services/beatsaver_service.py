import pybeatsaver

from src.kiyomi import BaseService, Kiyomi
from ..storage import UnitOfWork


class BeatSaverService(BaseService[UnitOfWork]):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, beatsaver: pybeatsaver.BeatSaverAPI):
        super().__init__(bot, uow)

        self.beatsaver = beatsaver
