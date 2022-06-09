from typing import Optional, List

from .achievement_cog import AchievementCog
from .services.achievements import Achievement


class AchievementsAPI(AchievementCog):
    async def get_best_achievement_in_group(self, group: str, member_id: int) -> Optional[Achievement]:
        return await self.user_achievement_service.get_best_completed_achievement_in_group(group, member_id)

    async def get_all_achievements_in_group(self, group: str, member_id: int) -> List[Achievement]:
        achievement_groups = await self.user_achievement_service.get_group_achievements(group, member_id)

        return achievement_groups[group]
