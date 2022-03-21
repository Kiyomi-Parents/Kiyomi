from .services import MemberAchievementRoleService
from src.kiyomi import BaseCog, Kiyomi


class AchievementRolesCog(BaseCog):
    def __init__(self, bot: Kiyomi, member_service: MemberAchievementRoleService):
        super().__init__(bot)

        self.member_service = member_service
