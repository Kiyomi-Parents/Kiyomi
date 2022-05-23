from .services.pfp_service import PFPService
from src.kiyomi import BaseCog, Kiyomi


class PFPSwitcherCog(BaseCog):
    def __init__(
            self,
            bot: Kiyomi,
            pfp_service: PFPService
    ):
        super().__init__(bot)

        self.pfp_service = pfp_service
