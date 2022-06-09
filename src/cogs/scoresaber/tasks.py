import pyscoresaber
from discord.ext import tasks

from src.kiyomi import BaseTasks
from src.kiyomi.utils import Utils
from src.log import Logger
from .services import ServiceUnitOfWork
from src.cogs.fancy_presence import FancyPresenceAPI


class Tasks(BaseTasks[ServiceUnitOfWork]):
    @tasks.loop(minutes=5)
    @Utils.time_task
    @Utils.discord_ready
    @FancyPresenceAPI.presence_task
    async def update_players(self):
        """Updating players"""
        players = await self.service_uow.players.get_all_players()
        Logger.log("Score Saber", f"Updating {len(players)} players")

        for player in players:
            await self.service_uow.players.update_player(player)

        await self.service_uow.save_changes()

    @tasks.loop(minutes=3)
    @Utils.time_task
    @Utils.discord_ready
    @FancyPresenceAPI.presence_task
    async def update_players_scores(self):
        """Updating scores"""
        players = await self.service_uow.players.get_all_players()
        Logger.log("Score Saber", f"Updating scores for {len(players)} players")

        for player in players:
            await self.service_uow.scores.update_player_scores(player)
            await self.service_uow.save_changes()

    @Utils.discord_ready
    async def init_live_score_feed(self):
        Logger.log("Score Saber", "Started listening to live score feed!")
        async for item in self.service_uow.scores.scoresaber.websocket():
            if isinstance(item, pyscoresaber.PlayerScore):
                player_score = item

                if await self.service_uow.players.player_exists(player_score.score.leaderboard_player_info.id):
                    await self.service_uow.scores.on_new_live_score_feed_score(player_score)
                    await self.service_uow.save_changes()
