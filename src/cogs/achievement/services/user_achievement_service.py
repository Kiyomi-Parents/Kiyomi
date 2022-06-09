from typing import List

from discord import Interaction
from discord.app_commands import Choice

from src.kiyomi.service.base_basic_service import BaseBasicService
from .achievements import Achievement
from .registry_service import RegistryService, AchievementGroups
from ..storage.storage_unit_of_work import StorageUnitOfWork
from src.kiyomi import Kiyomi
from src.cogs.general import GeneralAPI


class UserAchievementService(BaseBasicService[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork, registry_service: RegistryService):
        super().__init__(bot, storage_uow)

        self.registry_service = registry_service

    async def get_group_achievements(self, group: str, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = await general.get_member(member_id)

        return self.registry_service.get_achievements(group, member)

    async def get_group_completed(self, group: str, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = await general.get_member(member_id)

        return await self.registry_service.get_completed(group, member)

    async def get_all_achievements(self, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = await general.get_member(member_id)

        return self.registry_service.get_all_achievements(member)

    async def get_all_completed_achievements(self, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = await general.get_member(member_id)

        return await self.registry_service.get_all_completed(member)

    async def get_all_uncompleted_achievements(self, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = await general.get_member(member_id)

        return await self.registry_service.get_all_uncompleted(member)

    async def get_best_completed_achievement_in_group(self, group: str, member_id: int) -> Achievement:
        achievement_groups = await self.get_group_completed(group, member_id)

        best_achievement = None

        for achievement in achievement_groups[group]:
            if best_achievement is None:
                best_achievement = achievement
                continue

            if best_achievement.index > achievement.index:
                best_achievement = achievement

        return best_achievement

    async def get_all_groups(self, ctx: Interaction, current: str) -> List[Choice[str]]:
        choices = []

        for group in self.registry_service.get_generators():
            if current.lower() in group.lower():
                choices.append(Choice(name=group, value=group))

        return choices
