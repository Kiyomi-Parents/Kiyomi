from typing import List

import discord

from src.cogs.general import GeneralAPI
from src.log import Logger
from .achievement_roles_service import AchievementRolesService
from ..errors import UnableToCreateRole
from ..storage.model.achievement_role import AchievementRole
from ..storage.model.achievement_role_member import AchievementRoleMember
from src.cogs.achievement import AchievementsAPI
from src.cogs.achievement.services.achievements import Achievement
from src.cogs.settings import SettingsAPI
from src.cogs.general.errors import FailedToCreateRole, FailedToRemoveFromUser, RoleNotFound, FailedToAddToUser


class MemberAchievementRoleService(AchievementRolesService):
    roles = [
        {
            "group": "PP",
            "setting": "achievement_roles_pp"
        },
        {
            "group": "Rank",
            "setting": "achievement_roles_rank"
        }
    ]

    async def update_guild_roles(self, guild_id: int):
        general = self.bot.get_cog_api(GeneralAPI)

        guild_members = await general.get_members_in_guild(guild_id)

        for guild_member in guild_members:
            await self.update_member_roles(guild_member.guild_id, guild_member.member_id)

    async def update_member_roles(self, guild_id: int, member_id: int):
        settings = self.bot.get_cog_api(SettingsAPI)

        for role in self.roles:
            enabled = await settings.get(guild_id, role.get("setting"))

            if enabled:
                await self.update_member_achievement_roles(guild_id, member_id, role.get("group"))
            else:
                await self.remove_all_member_group_roles(
                        guild_id,
                        member_id,
                        role.get("group")
                )

    async def update_member_achievement_roles(self, guild_id: int, member_id: int, group: str):
        achievements = self.bot.get_cog_api(AchievementsAPI)

        # Get Achievement
        achievement = await achievements.get_best_achievement_in_group(group, member_id)

        if achievement is None:
            Logger.log("Achievement Roles", f"No completed achievements for group {group}")
            return

        # Get achievement role or create it
        achievement_role = await self.get_achievement_role(guild_id, group, achievement)

        # Check if member already has the achievement role
        if await self.member_has_role(guild_id, member_id, achievement_role):
            Logger.log(
                    "AchievementRoles", f"Member {member_id} already has role {achievement_role} in Guild {guild_id}. "
                                        f"SKIPPING!"
            )
            return

        # Remove all other achievement roles from the member
        await self.remove_all_member_group_roles(guild_id, member_id, group)

        # Give member the achievement role
        await self.give_member_role(guild_id, member_id, achievement_role)

    async def give_member_role(self, guild_id: int, member_id: int, achievement_role: AchievementRole):
        general = self.bot.get_cog_api(GeneralAPI)

        try:
            await general.add_role_to_member(
                    guild_id,
                    member_id,
                    achievement_role.role_id,
                    "Auto added by Achievement Roles"
            )

            async with self.uow:
                await self.uow.achievement_role_members.add(
                        AchievementRoleMember(guild_id, member_id, achievement_role.id)
                )
        except FailedToAddToUser as error:
            await error.handle(bot=self.bot)

    async def remove_member_role(
            self,
            guild_id: int,
            member_id: int,
            achievement_role_member: AchievementRoleMember
    ) -> None:
        general = self.bot.get_cog_api(GeneralAPI)

        try:
            await general.remove_role_from_member(
                    guild_id,
                    member_id,
                    achievement_role_member.achievement_role.role_id,
                    "Auto removed by Achievement Roles"
            )
        except FailedToRemoveFromUser as error:
            await error.handle(bot=self.bot)
        finally:
            async with self.uow:
                await self.uow.achievement_role_members.remove(achievement_role_member)

    async def get_all_member_group_roles(self, guild_id: int, member_id: int, group: str) -> List[AchievementRoleMember]:
        achievement_roles = await self.uow.achievement_roles.get_all_by_guild_id_and_group(guild_id, group)

        achievement_role_member = []

        for achievement_role in achievement_roles:
            role_member = await self.uow.achievement_role_members.get_by_all(guild_id, member_id, achievement_role.id)

            if role_member is not None:
                achievement_role_member.append(role_member)

        return achievement_role_member

    async def get_achievement_role(self, guild_id: int, group: str, achievement: Achievement) -> AchievementRole:
        achievement_role = await self.uow.achievement_roles.get_by_guild_id_and_group_and_identifier(
                guild_id,
                group,
                achievement.identifier
        )

        if achievement_role is None:
            achievement_role = await self.create_achievement_role(guild_id, group, achievement)

        if not await self.exists_achievement_role(achievement_role):
            async with self.uow:
                await self.uow.achievement_roles.remove(achievement_role)
                achievement_role = await self.create_achievement_role(guild_id, group, achievement)

        if achievement_role is None:
            async with self.uow:
                await self.uow.achievement_roles.remove(achievement_role)

            raise UnableToCreateRole(guild_id, group, achievement)

        return achievement_role

    async def exists_achievement_role(self, achievement_role: AchievementRole) -> bool:
        general = self.bot.get_cog_api(GeneralAPI)

        try:
            await general.get_role(achievement_role.guild_id, achievement_role.role_id)
            return True
        except RoleNotFound as error:
            await error.handle(
                    bot=self.bot,
                    message=f"[{achievement_role.group}] Role {achievement_role.identifier} "
                            f"(%role_id%) "
                            f"doesn't exist on Guild %guild_id%"
            )

        return False

    async def create_achievement_role(self, guild_id: int, group: str, achievement: Achievement) -> AchievementRole:
        general = self.bot.get_cog_api(GeneralAPI)

        try:
            role = await general.create_role(
                    guild_id,
                    achievement.name,
                    discord.Color.random(),
                    False,
                    "Auto created by Achievement Roles"
            )

            async with self.uow:
                return await self.uow.achievement_roles.add(
                        AchievementRole(guild_id, role.id, group, achievement.identifier)
                )
        except FailedToCreateRole as error:
            raise UnableToCreateRole(guild_id, group, achievement) from error

    async def remove_all_member_roles(self, guild_id: int, member_id: int):
        for role in self.roles:
            await self.remove_all_member_group_roles(guild_id, member_id, role.get("group"))

    async def remove_all_member_group_roles(self, guild_id: int, member_id: int, group: str):
        achievement_role_members = await self.get_all_member_group_roles(guild_id, member_id, group)

        for achievement_role_member in achievement_role_members:
            await self.remove_member_role(guild_id, member_id, achievement_role_member)

    async def member_has_role(self, guild_id: int, member_id: int, achievement_role: AchievementRole) -> bool:
        achievement_role_member = await self.uow.achievement_role_members.get_by_all(
                guild_id,
                member_id,
                achievement_role.id
        )

        if achievement_role_member is not None:
            # Check if member has role on discord
            general = self.bot.get_cog_api(GeneralAPI)
            if not await general.member_has_role(
                    guild_id,
                    member_id,
                    achievement_role.role_id
            ):
                async with self.uow:
                    await self.uow.achievement_role_members.remove(achievement_role_member)

                return False

            return True

        return False
