import pyscoresaber

from src.kiyomi import Kiyomi, BaseService
from ..storage import UnitOfWork


class ScoreSaberService(BaseService[UnitOfWork]):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, scoresaber: pyscoresaber.ScoreSaberAPI):
        super().__init__(bot, uow)

        self.scoresaber = scoresaber

    async def start_scoresaber_api_client(self):
        await self.scoresaber.start()
