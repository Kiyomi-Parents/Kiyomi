from typing import List

import discord
from discord import OptionChoice

from .registry import Registry, AchievementGroups, Achievement
from .storage.uow import UnitOfWork


class Actions:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.registry = Registry(uow)

    def get_group_achievements(self, group: str, member_id: int) -> AchievementGroups:
        general = self.uow.bot.get_cog("GeneralAPI")
        member = general.get_member(member_id)

        return self.registry.get_achievements(group, member)

    def get_group_completed(self, group: str, member_id: int) -> AchievementGroups:
        general = self.uow.bot.get_cog("GeneralAPI")
        member = general.get_member(member_id)

        return self.registry.get_completed(group, member)

    def get_all_achievements(self, member_id: int) -> AchievementGroups:
        general = self.uow.bot.get_cog("GeneralAPI")
        member = general.get_member(member_id)

        return self.registry.get_all_achievements(member)

    def get_all_completed_achievements(self, member_id: int) -> AchievementGroups:
        general = self.uow.bot.get_cog("GeneralAPI")
        member = general.get_member(member_id)

        return self.registry.get_all_completed(member)

    def get_all_uncompleted_achievements(self, member_id: int) -> AchievementGroups:
        general = self.uow.bot.get_cog("GeneralAPI")
        member = general.get_member(member_id)

        return self.registry.get_all_uncompleted(member)

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

        for group in self.registry.get_generators():
            choices.append(OptionChoice(group, group))

        return choices
