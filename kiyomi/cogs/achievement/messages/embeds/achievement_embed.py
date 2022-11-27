from kiyomi.base_embed import BaseEmbed

from kiyomi import Kiyomi


class AchievementEmbed(BaseEmbed):
    def __init__(self, bot: Kiyomi):
        super().__init__(bot)
