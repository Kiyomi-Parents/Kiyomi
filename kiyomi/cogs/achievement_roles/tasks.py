import asyncio

from discord.ext import tasks

from kiyomi.cogs.general import GeneralAPI
from kiyomi.cogs.fancy_presence import FancyPresenceAPI
from kiyomi.utils import Utils
from kiyomi import BaseTasks
from .services import ServiceUnitOfWork


class Tasks(BaseTasks[ServiceUnitOfWork]):
    @tasks.loop(minutes=5)
    @Utils.time_task
    @Utils.discord_ready
    @FancyPresenceAPI.presence_task
    async def update_member_roles(self):
        """Updating roles"""
        async with self.bot.get_cog_api(GeneralAPI) as general:
            guild_members = await general.get_all_guild_members()

        await_list = []
        for guild_member in guild_members:
            await_list.append(
                    self.service_uow.memberAchievementRoles.update_member_roles(
                            guild_member.guild_id,
                            guild_member.member_id
                    )
            )
        await asyncio.gather(*await_list)

        await self.service_uow.save_changes()
