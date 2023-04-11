import logging
from datetime import datetime

import pyscoresaber
import timeago
from discord.ext import tasks

from kiyomi.cogs.fancy_presence import FancyPresenceAPI
from kiyomi.utils import Utils
from kiyomi import BaseTasks
from .services import ServiceUnitOfWork

_logger = logging.getLogger(__name__)


class Tasks(BaseTasks[ServiceUnitOfWork]):
    @tasks.loop(minutes=5)
    @Utils.time_task
    @Utils.discord_ready
    @FancyPresenceAPI.presence_task
    async def update_players(self):
        """Updating players"""
        players = await self.service_uow.players.get_all_player_ids()
        _logger.info("Score Saber", f"Updating {len(players)} players")

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
        _logger.info("Score Saber", f"Updating scores for {len(players)} players")

        for player in players:
            start_time = datetime.now()
            await self.service_uow.scores.update_player_scores(player)
            end_time = datetime.now()
            _logger.info("Score Saber", f"Finished updating {player} scores in"
                                        f" {timeago.format(end_time, start_time, locale='en_short')}")

            await self.service_uow.save_changes()

    @Utils.discord_ready
    async def init_live_score_feed(self):
        _logger.info("Score Saber", "Started listening to live score feed!")
        async for item in self.service_uow.scores.scoresaber.websocket():
            if isinstance(item, pyscoresaber.PlayerScore):
                player_score = item

                if await self.service_uow.players.exists(player_score.score.leaderboard_player_info.id):
                    await self.service_uow.scores.on_new_live_score_feed_score(player_score)
                    await self.service_uow.save_changes()

        await self.service_uow.close()
