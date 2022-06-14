from discord.ext import tasks

from src.cogs.pfp_switcher import ServiceUnitOfWork
from src.kiyomi import BaseTasks, Utils


class Tasks(BaseTasks[ServiceUnitOfWork]):
    @tasks.loop(minutes=1)
    @Utils.discord_ready
    async def update_profile_picture(self):
        """Update Kiyomi's profile picture"""
        profile_picture = self.service_uow.profile_pictures.get_pfp()

        if not self.service_uow.profile_pictures.is_current_pfp(profile_picture):
            await self.service_uow.profile_pictures.set_pfp(profile_picture)

    @update_profile_picture.after_loop
    async def update_profile_picture_after(self):
        await self.service_uow.close()
