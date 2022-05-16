from src.kiyomi import Kiyomi
from src.kiyomi.base_embed import BaseEmbed


class AchievementEmbed(BaseEmbed):
    def __init__(self, bot: Kiyomi):
        super().__init__(bot)
