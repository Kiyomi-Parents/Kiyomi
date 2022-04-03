from .services.user_achievement_service import UserAchievementService
from src.kiyomi import BaseCog, Kiyomi


class AchievementCog(BaseCog):
    def __init__(self, bot: Kiyomi, user_achievement_service: UserAchievementService):
        super().__init__(bot)

        self.user_achievement_service = user_achievement_service
