from typing import Optional, List

from discord.ext import commands

from .actions import Actions
from .registry import Achievement
from .storage.unit_of_work import UnitOfWork


class AchievementsAPI(commands.Cog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

    def get_best_achievement_in_group(self, group: str, member_id: int) -> Optional[Achievement]:
        return self.actions.get_best_completed_achievement_in_group(group, member_id)

    def get_all_achievements_in_group(self, group: str, member_id: int) -> List[Achievement]:
        achievement_groups = self.actions.get_group_achievements(group, member_id)

        return achievement_groups[group]
