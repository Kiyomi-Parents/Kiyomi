from discord.ext import tasks

from src.cogs.general import GeneralAPI
from src.kiyomi import BaseTasks, Kiyomi
from src.kiyomi.utils import Utils
from .services import MemberAchievementRoleService
from src.cogs.fancy_presence import FancyPresenceAPI


class Tasks(BaseTasks):
    def __init__(self, bot: Kiyomi, member_service: MemberAchievementRoleService):
        super().__init__(bot)

        self.member_service = member_service

    @tasks.loop(minutes=5)
    @Utils.time_task
    @Utils.discord_ready
    @FancyPresenceAPI.presence_task
    async def update_member_roles(self):
        """Updating roles"""
        general = self.bot.get_cog_api(GeneralAPI)

        guild_members = await general.get_all_guild_members()

        for guild_member in guild_members:
            await self.member_service.update_member_roles(guild_member.guild_id, guild_member.member_id)
