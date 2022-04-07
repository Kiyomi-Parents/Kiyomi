from discord.ext import tasks

from src.cogs.scoresaber import ScoreSaberAPI
from src.kiyomi import Kiyomi, BaseTasks
from src.kiyomi.utils import Utils
from src.log import Logger
from .services.notification_service import NotificationService
from src.cogs.fancy_presence import FancyPresenceAPI


class Tasks(BaseTasks):

    def __init__(self, bot: Kiyomi, notification_service: NotificationService):
        super().__init__(bot)

        self.notification_service = notification_service

    @tasks.loop(minutes=1)
    @Utils.time_task
    @Utils.discord_ready
    @FancyPresenceAPI.presence_task
    async def send_notifications(self) -> None:
        """Sending notifications"""
        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        players = scoresaber.get_players()
        Logger.log("task", f"Sending notifications for {len(players)} players")

        for player in players:
            for guild in player.guilds:
                await self.notification_service.send_notification(guild, player)

