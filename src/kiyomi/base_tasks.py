from .kiyomi import Kiyomi


class BaseTasks:

    def __init__(self, bot: Kiyomi):
        self.bot = bot
