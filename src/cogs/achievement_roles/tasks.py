import asyncio
from typing import List

import discord
from discord.ext import tasks

from src.log import Logger
from src.utils import Utils
from .storage.model import AchievementRole, AchievementRoleMember
from .storage.uow import UnitOfWork
from src.cogs.achievements.registry import Achievement
from src.cogs.general.storage.model import GuildMember


class Tasks:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.update_member_roles_lock = asyncio.Lock()

    @tasks.loop(minutes=1)
    @Utils.time_task
    @Utils.discord_ready
    @Utils.update_tasks_list
    async def update_member_roles(self):
        """updating member roles"""
        async with self.update_member_roles_lock:
            general = self.uow.bot.get_cog("GeneralAPI")
            settings = self.uow.bot.get_cog("SettingsAPI")

            guild_members = general.get_all_guild_members()

            for guild_member in guild_members:
                achievement_roles_pp = settings.get(guild_member.guild.id, "achievement_roles_pp")

                if achievement_roles_pp:
                    await self.update_member_pp_roles(guild_member)

    async def update_member_pp_roles(self, guild_member: GuildMember):
        group = "PP"
        achievements = self.uow.bot.get_cog("AchievementsAPI")

        # Get Achievement
        achievement = achievements.get_best_achievement_in_group(group, guild_member.member.id)

        if achievement is None:
            Logger.log("AchievementRoles", f"No completed achievements for group {group}")
            return

        # Get achievement role or create it
        achievement_role = await self.get_achievement_role(guild_member.guild_id, group, achievement)

        # Check if member already has the achievement role
        achievement_role_member = self.uow.achievement_role_member_repo.get_by_all(guild_member.guild_id,
                                                                                   guild_member.member_id,
                                                                                   achievement_role.id)

        if achievement_role_member is not None:
            Logger.log("AchievementRoles", f"{guild_member.member.name} already has role {achievement_role}. SKIPPING!")
            return

        # Remove all other achievement roles from the member
        remove_role_members = self.get_all_member_group_roles(guild_member.guild_id, guild_member.member_id, group)

        for remove_role_member in remove_role_members:
            await self.remove_member_role(guild_member.guild_id, guild_member.member_id, remove_role_member)

        # Give member the achievement role
        await self.give_member_role(guild_member.guild_id, guild_member.member_id, achievement_role)

    async def give_member_role(self, guild_id: int, member_id: int, achievement_role: AchievementRole):
        general = self.uow.bot.get_cog("GeneralAPI")

        await general.add_role_to_member(guild_id,
                                         member_id,
                                         achievement_role.role_id,
                                         "Auto added by Achievement Roles"
                                         )

        self.uow.achievement_role_member_repo.add(AchievementRoleMember(guild_id, member_id, achievement_role.id))

    async def remove_member_role(self, guild_id: int, member_id: int,
                                 achievement_role_member: AchievementRoleMember) -> None:
        general = self.uow.bot.get_cog("GeneralAPI")

        await general.remove_role_from_member(
            guild_id,
            member_id,
            achievement_role_member.achievement_role.id,
            "Auto removed by Achievement Roles"
        )

        self.uow.achievement_role_member_repo.remove(achievement_role_member)

    def get_all_member_group_roles(self, guild_id: int, member_id: int, group: str) -> List[AchievementRoleMember]:
        achievement_roles = self.uow.achievement_role_repo.get_all_by_guild_id_and_group(guild_id, group)

        achievement_role_member = []

        for achievement_role in achievement_roles:
            role_member = self.uow.achievement_role_member_repo.get_by_all(guild_id, member_id, achievement_role.id)

            if role_member is not None:
                achievement_role_member.append(role_member)

        return achievement_role_member

    async def get_achievement_role(self, guild_id: int, group: str, achievement: Achievement) -> AchievementRole:
        achievement_role = self.uow.achievement_role_repo.get_by_guild_id_and_group_and_identifier(
            guild_id,
            group,
            achievement.identifier
        )

        if achievement_role is None:
            achievement_role = await self.create_achievement_role(guild_id, group, achievement)

        return achievement_role

    async def create_achievement_role(self, guild_id: int, group: str, achievement: Achievement) -> AchievementRole:
        general = self.uow.bot.get_cog("GeneralAPI")

        role = await general.create_role(
            guild_id,
            achievement.name,
            discord.Color.random(),
            False,
            "Auto created by Achievement Roles"
        )

        return self.uow.achievement_role_repo.add(AchievementRole(guild_id, role.id, group, achievement.identifier))
