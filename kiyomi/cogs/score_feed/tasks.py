import logging

from discord.ext import tasks

from kiyomi.cogs.scoresaber import ScoreSaberAPI
from kiyomi.cogs.fancy_presence import FancyPresenceAPI
from kiyomi.utils import Utils
from kiyomi import BaseTasks
from .services import ServiceUnitOfWork

_logger = logging.getLogger(__name__)


class Tasks(BaseTasks[ServiceUnitOfWork]):
    @tasks.loop(minutes=1)
    @Utils.time_task
    @Utils.discord_ready
    @FancyPresenceAPI.presence_task
    async def send_notifications(self) -> None:
        """Sending notifications"""
        async with self.bot.get_cog_api(ScoreSaberAPI) as scoresaber:
            players = await scoresaber.get_players()

        _logger.info("task", f"Sending notifications for {len(players)} players")

        for player in players:
            for guild in player.guilds:
                await self.service_uow.notifications.send_notification(guild, player)
                await self.service_uow.save_changes()

    @send_notifications.after_loop
    async def send_notifications_after(self):
        await self.service_uow.close()