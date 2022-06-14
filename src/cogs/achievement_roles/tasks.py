from discord.ext import tasks

from src.cogs.general import GeneralAPI
from src.kiyomi import BaseTasks
from src.kiyomi.utils import Utils
from .services import ServiceUnitOfWork
from src.cogs.fancy_presence import FancyPresenceAPI


class Tasks(BaseTasks[ServiceUnitOfWork]):
    @tasks.loop(minutes=5)
    @Utils.time_task
    @Utils.discord_ready
    @FancyPresenceAPI.presence_task
    async def update_member_roles(self):
        """Updating roles"""
        general = self.bot.get_cog_api(GeneralAPI)

        guild_members = await general.get_all_guild_members()

        for guild_member in guild_members:
            await self.service_uow.memberAchievementRoles.update_member_roles(guild_member.guild_id, guild_member.member_id)

        await self.service_uow.save_changes()

    @update_member_roles.after_loop
    async def update_member_roles_after(self):
        await self.service_uow.close()
