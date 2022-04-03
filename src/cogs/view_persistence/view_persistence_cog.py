from src.cogs.view_persistence import MessageViewService
from src.kiyomi import BaseCog, Kiyomi


class ViewPersistenceCog(BaseCog):
    def __init__(self, bot: Kiyomi, message_view_service: MessageViewService):
        super().__init__(bot)

        self.message_view_service = message_view_service
