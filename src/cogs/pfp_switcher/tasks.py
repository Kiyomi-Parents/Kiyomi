from discord.ext import tasks

from src.cogs.pfp_switcher import PFPService
from src.kiyomi import BaseTasks, Kiyomi, Utils


class Tasks(BaseTasks):

    def __init__(self, bot: Kiyomi, pfp_service: PFPService):
        super().__init__(bot)

        self.pfp_service = pfp_service

    @tasks.loop(minutes=1)
    @Utils.discord_ready
    async def update_profile_picture(self):
        """Update Kiyomi's profile picture"""
        profile_picture = self.pfp_service.get_pfp()

        if not self.pfp_service.is_current_pfp(profile_picture):
            await self.pfp_service.set_pfp(profile_picture)
