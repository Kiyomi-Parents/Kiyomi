from discord.ext import tasks

from src.cogs.scoresaber import ScoreSaberAPI
from src.kiyomi import BaseTasks
from src.kiyomi.utils import Utils
from src.log import Logger
from .services import ServiceUnitOfWork
from src.cogs.fancy_presence import FancyPresenceAPI


class Tasks(BaseTasks[ServiceUnitOfWork]):
    @tasks.loop(minutes=1)
    @Utils.time_task
    @Utils.discord_ready
    @FancyPresenceAPI.presence_task
    async def send_notifications(self) -> None:
        """Sending notifications"""
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        players = await scoresaber.get_players()
        Logger.log("task", f"Sending notifications for {len(players)} players")

        for player in players:
            for guild in player.guilds:
                await self.service_uow.notifications.send_notification(guild, player)
                await self.service_uow.save_changes()

    @send_notifications.after_loop
    async def send_notifications_after(self):
        await self.service_uow.close()