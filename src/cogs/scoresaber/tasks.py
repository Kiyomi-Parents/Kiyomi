from discord.ext import tasks

from src.kiyomi import Kiyomi, BaseTasks
from src.kiyomi.utils import Utils
from src.log import Logger
from .services import PlayerService, ScoreService


class Tasks(BaseTasks):

    def __init__(self, bot: Kiyomi, player_service: PlayerService, score_service: ScoreService):
        super().__init__(bot)

        self.player_service = player_service
        self.score_service = score_service

    @tasks.loop(minutes=10)
    @Utils.time_task
    @Utils.discord_ready
    @Utils.update_tasks_list
    async def update_players(self):
        """Updating players"""
        players = await self.player_service.get_all_players()
        Logger.log("task", f"Updating {len(players)} players")

        for player in players:
            await self.player_service.update_player(player)

    @tasks.loop(minutes=2)
    @Utils.time_task
    @Utils.discord_ready
    @Utils.update_tasks_list
    async def update_players_scores(self):
        """Updating scores"""
        players = await self.player_service.get_all_players()
        Logger.log("task", f"Updating scores for {len(players)} players")

        for player in players:
            await self.score_service.update_player_scores(player)
