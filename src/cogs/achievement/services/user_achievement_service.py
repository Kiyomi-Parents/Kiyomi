from typing import List

import discord
from discord import OptionChoice

from .achievement_service import AchievementService
from .achievements import Achievement
from .registry_service import RegistryService, AchievementGroups
from ..storage.unit_of_work import UnitOfWork
from src.kiyomi import Kiyomi
from src.cogs.general import GeneralAPI


class UserAchievementService(AchievementService):
    def __init__(self, bot: Kiyomi, uow: UnitOfWork, registry_service: RegistryService):
        super().__init__(bot, uow)

        self.registry_service = registry_service

    def get_group_achievements(self, group: str, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = general.get_member(member_id)

        return self.registry_service.get_achievements(group, member)

    def get_group_completed(self, group: str, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = general.get_member(member_id)

        return self.registry_service.get_completed(group, member)

    def get_all_achievements(self, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = general.get_member(member_id)

        return self.registry_service.get_all_achievements(member)

    def get_all_completed_achievements(self, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = general.get_member(member_id)

        return self.registry_service.get_all_completed(member)

    def get_all_uncompleted_achievements(self, member_id: int) -> AchievementGroups:
        general = self.bot.get_cog_api(GeneralAPI)
        member = general.get_member(member_id)

        return self.registry_service.get_all_uncompleted(member)

    def get_best_completed_achievement_in_group(self, group: str, member_id: int) -> Achievement:
        achievement_groups = self.get_group_completed(group, member_id)

        best_achievement = None

        for achievement in achievement_groups[group]:
            if best_achievement is None:
                best_achievement = achievement
                continue

            if best_achievement.index > achievement.index:
                best_achievement = achievement

        return best_achievement

    async def get_all_groups(self, ctx: discord.AutocompleteContext) -> List[OptionChoice]:
        choices = []

        for group in self.registry_service.get_generators():
            choices.append(OptionChoice(group, group))

        return choices
