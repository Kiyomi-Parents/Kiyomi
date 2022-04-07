from src.cogs.fancy_presence.services.presence_service import PresenceService
from src.kiyomi import BaseCog, Kiyomi


class FancyPresenceCog(BaseCog):
    def __init__(self, bot: Kiyomi, presence_service: PresenceService):
        super().__init__(bot)

        self.presence_service = presence_service
