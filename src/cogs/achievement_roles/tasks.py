from discord.ext import tasks

from src.cogs.general import GeneralAPI
from src.cogs.settings import SettingsAPI
from src.kiyomi import BaseTasks, Kiyomi
from src.kiyomi.utils import Utils
from .services import MemberAchievementRoleService


class Tasks(BaseTasks):

    def __init__(self, bot: Kiyomi, member_service: MemberAchievementRoleService):
        super().__init__(bot)

        self.member_service = member_service

    # TODO: Better error handling
    @tasks.loop(minutes=5)
    @Utils.time_task
    @Utils.discord_ready
    @Utils.update_tasks_list
    async def update_member_roles(self):
        """Updating roles"""
        general = self.bot.get_cog_api(GeneralAPI)
        settings = self.bot.get_cog_api(SettingsAPI)

        guild_members = general.get_all_guild_members()

        for guild_member in guild_members:
            achievement_roles_pp = settings.get(guild_member.guild.id, "achievement_roles_pp")

            if achievement_roles_pp:
                await self.member_service.update_member_pp_roles(guild_member)


