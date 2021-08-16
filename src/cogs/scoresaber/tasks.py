import asyncio
from typing import List

import pyscoresaber
from discord.ext import tasks

from .storage.uow import UnitOfWork
from .storage.model.player import Player
from .storage.model.score import Score
from src.log import Logger
from src.utils import Utils


class Tasks:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.update_players_lock = asyncio.Lock()
        self.update_players_scores_lock = asyncio.Lock()

    @tasks.loop(minutes=30)
    @Utils.time_task
    @Utils.discord_ready
    async def update_players(self):
        async with self.update_players_lock:
            players = self.uow.player_repo.get_all()
            Logger.log("task", f"Updating {len(players)} players")

            for player in players:
                await self.update_player(player)

    async def update_player(self, player: Player):
        try:
            new_player = await self.uow.scoresaber.get_player_basic(player.id)

            self.uow.player_repo.update(Player(new_player))
        except pyscoresaber.NotFoundException:
            Logger.log(player, "Could not find at ScoreSaber")

    @tasks.loop(minutes=2)
    @Utils.time_task
    @Utils.discord_ready
    @Utils.update_tasks_list
    async def update_players_scores(self):
        """updating player scores"""
        async with self.update_players_scores_lock:
            players = self.uow.player_repo.get_all()
            Logger.log("task", f"Updating scores for {len(players)} players")

            for player in players:
                await self.update_player_scores(player)

    async def update_player_scores(self, player: Player):
        new_scores = await self.get_all_recent_scores(player)
        Logger.log(player, f"Got {len(new_scores)} new recent scores from ScoreSaber")

        # Add new scores to database
        self.uow.player_repo.add_scores(player, new_scores)

        # Get db scores from recent scores
        scores = self.uow.score_repo.get_scores(new_scores)

        # Emit event for new scores
        self.uow.bot.events.emit("on_new_scores", scores)

    async def get_all_recent_scores(self, player: Player) -> List[Score]:
        new_scores = []
        last_new_scores_len = -1
        page = 1

        while len(new_scores) != last_new_scores_len:
            last_new_scores_len = len(new_scores)

            try:
                recent_scores = await self.uow.scoresaber.get_recent_scores(player.id, page)
                Logger.log(player, f"Got {len(recent_scores)} recent scores from ScoreSaber page {page}")

                for recent_score in recent_scores:
                    new_score = Score(recent_score)

                    if self.uow.score_repo.is_score_new(new_score):
                        new_scores.append(new_score)

            except pyscoresaber.NotFoundException:
                Logger.log(player, "Could not find scores on ScoreSaber")
                break

            page += 1

        return new_scores
