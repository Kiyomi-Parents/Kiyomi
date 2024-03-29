from discord import Permissions
from discord.ext import commands

from kiyomi.cogs.settings.storage.model.toggle_setting import ToggleSetting
from kiyomi.cogs.general.storage.model.guild_member import GuildMember
from kiyomi.cogs.settings.storage.model.abstract_setting import AbstractSetting
from .services import ServiceUnitOfWork
from kiyomi import BaseCog
from ..general.storage.model.member_role import MemberRole
from ..general.storage.model.role import Role


class AchievementRoles(BaseCog[ServiceUnitOfWork], name="Achievement Roles"):
    def register_events(self):
        @self.bot.events.on("on_new_player")
        async def register_member(guild_member: GuildMember):
            await self._service_uow.memberAchievementRoles.update_member_roles(guild_member.guild_id, guild_member.member_id)
            await self._service_uow.save_changes()
            await self._service_uow.close()

        @self.bot.events.on("on_remove_player")
        async def unregister_member(guild_member: GuildMember):
            await self._service_uow.memberAchievementRoles.remove_all_member_roles(
                guild_member.guild_id, guild_member.member_id
            )
            await self._service_uow.save_changes()
            await self._service_uow.close()

        @self.bot.events.on("on_setting_change")
        async def update_roles(setting: AbstractSetting):
            cog_settings = ["achievement_roles_pp", "achievement_roles_rank"]

            if setting.name in cog_settings:
                await self._service_uow.memberAchievementRoles.update_guild_roles(setting.guild_id)

            await self._service_uow.save_changes()
            await self._service_uow.close()

        @self.bot.events.on("on_member_role_removed")
        async def member_role_removed(member_role: MemberRole):
            await self._service_uow.memberAchievementRoles.update_member_roles(member_role.guild_id, member_role.member_id)
            await self._service_uow.save_changes()
            await self._service_uow.close()

        @self.bot.events.on("on_guild_role_removed")
        async def guild_role_removed(role: Role):
            await self._service_uow.memberAchievementRoles.update_guild_roles(role.guild_id)
            await self._service_uow.save_changes()
            await self._service_uow.close()

    @commands.Cog.listener()
    async def on_ready(self):
        permissions = Permissions(manage_roles=True)

        settings = [
            ToggleSetting.create(self.__cog_name__, "Roles based on PP", "achievement_roles_pp", permissions),
            ToggleSetting.create(self.__cog_name__, "Roles based on rank", "achievement_roles_rank", permissions),
        ]

        self.bot.events.emit("setting_register", settings)
