from Kiyomi import Kiyomi
from .repository import AchievementRoleRepository, AchievementRoleMemberRepository


class UnitOfWork:

    def __init__(self, bot: Kiyomi):
        self.achievement_role_repo = AchievementRoleRepository(bot.database)
        self.achievement_role_member_repo = AchievementRoleMemberRepository(bot.database)
        self.bot = bot
