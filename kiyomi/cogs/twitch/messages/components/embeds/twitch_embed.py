from discord import Embed

from kiyomi import Kiyomi


class TwitchEmbed(Embed):
    def __init__(self, bot: Kiyomi):
        super().__init__()

        self.bot = bot
