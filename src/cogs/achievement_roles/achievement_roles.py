from discord import Permissions
from discord.ext import commands

from src.cogs.settings.storage.model.toggle_setting import ToggleSetting
from .services.member_achievement_role_service import MemberAchievementRoleService
from .achievement_roles_cog import AchievementRolesCog
from src.cogs.general.storage.model.guild_member import GuildMember
from src.kiyomi import Kiyomi
from ..general.storage.model.member_role import MemberRole
from ..general.storage.model.role import Role
from ..settings.storage import AbstractSetting


class AchievementRoles(AchievementRolesCog, name="Achievement Roles"):
    def __init__(self, bot: Kiyomi, member_service: MemberAchievementRoleService):
        super().__init__(bot, member_service)

        # Register events
        self.events()

    def events(self):
        @self.bot.events.on("on_new_player")
        async def register_member(guild_member: GuildMember):
            await self.member_service.update_member_roles(guild_member.guild_id, guild_member.member_id)

        @self.bot.events.on("on_remove_player")
        async def unregister_member(guild_member: GuildMember):
            await self.member_service.remove_all_member_roles(guild_member.guild_id, guild_member.member_id)

        @self.bot.events.on("on_setting_change")
        async def update_roles(setting: AbstractSetting):
            cog_settings = ["achievement_roles_pp", "achievement_roles_rank"]

            if setting.name in cog_settings:
                await self.member_service.update_guild_roles(setting.guild_id)

        @self.bot.events.on("on_member_role_removed")
        async def member_role_removed(member_role: MemberRole):
            await self.member_service.update_member_roles(member_role.guild_id, member_role.member_id)

        @self.bot.events.on("on_guild_role_removed")
        async def guild_role_removed(role: Role):
            await self.member_service.update_guild_roles(role.guild_id)

    @commands.Cog.listener()
    async def on_ready(self):
        permissions = Permissions(manage_roles=True)

        settings = [
            ToggleSetting.create("Roles based on PP", "achievement_roles_pp", permissions),
            ToggleSetting.create("Roles based on rank", "achievement_roles_rank", permissions),
        ]

        self.bot.events.emit("setting_register", settings)
