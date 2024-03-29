from discord.ext import tasks

from kiyomi.cogs.pfp_switcher import ServiceUnitOfWork
from kiyomi import BaseTasks, Utils


class Tasks(BaseTasks[ServiceUnitOfWork]):
    @tasks.loop(minutes=1)
    @Utils.discord_ready
    async def update_profile_picture(self):
        """Update Kiyomi's profile picture"""
        profile_picture = self.service_uow.profile_pictures.get_pfp()

        if not self.service_uow.profile_pictures.is_current_pfp(profile_picture):
            await self.service_uow.profile_pictures.set_pfp(profile_picture)
