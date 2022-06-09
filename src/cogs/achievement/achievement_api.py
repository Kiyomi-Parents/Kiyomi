from typing import Optional, List

from .services import ServiceUnitOfWork
from .services.achievements import Achievement
from src.kiyomi import BaseCog


class AchievementsAPI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    async def get_best_achievement_in_group(self, group: str, member_id: int) -> Optional[Achievement]:
        return await self.service_uow.user_achievements.get_best_completed_achievement_in_group(group, member_id)

    async def get_all_achievements_in_group(self, group: str, member_id: int) -> List[Achievement]:
        achievement_groups = await self.service_uow.user_achievements.get_group_achievements(group, member_id)

        return achievement_groups[group]
