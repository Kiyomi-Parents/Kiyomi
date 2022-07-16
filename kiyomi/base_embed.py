from discord import Embed

from .kiyomi import Kiyomi


class BaseEmbed(Embed):
    def __init__(self, bot: Kiyomi):
        super().__init__()

        self.bot = bot

    async def after_init(self):
        pass
