import logging

from kiyomi.cogs.scoresaber import ScoreSaberAPI
from kiyomi.cogs.general.storage.model.guild import Guild
from kiyomi.cogs.scoresaber.storage.model.player import Player
from kiyomi import BaseService
from ..storage import StorageUnitOfWork
from ..storage.model.sent_score import SentScore
from ..storage.repository.sent_score_repository import SentScoreRepository

_logger = logging.getLogger(__name__)


class SentScoreService(BaseService[SentScore, SentScoreRepository, StorageUnitOfWork]):
    async def mark_all_guild_scores_sent(self, guild_id: int):
        async with self.bot.get_cog_api(ScoreSaberAPI) as scoresaber:
            guild_players = await scoresaber.get_guild_players_by_guild(guild_id)

        if len(guild_players) == 0:
            return

        _logger.info(
            guild_players[0].guild,
            f"Marking scores sent for {len(guild_players)} players",
        )

        for guild_player in guild_players:
            await self.mark_player_scores_sent(guild_player.guild.id, guild_player.player.id)

    async def mark_all_player_scores_sent(self, player: Player):
        _logger.info(player, "Marking all scores as sent")

        for guild in player.guilds:
            await self.mark_player_scores_sent(guild.id, player.id)

    async def mark_player_scores_sent(self, guild_id: int, player_id: str):
        scores = await self.storage_uow.sent_scores.get_unsent_scores(guild_id, player_id)

        _logger.info(player_id, f"Marking {len(scores)} scores as sent in {guild_id}")

        sent_scores = []
        for score in scores:
            sent_scores.append(SentScore(score.id, guild_id))

        if len(sent_scores) != 0:
            await self.storage_uow.sent_scores.add_all(sent_scores)

    async def should_send_scores(self, guild: Guild, player: Player):
        sent_scores = await self.storage_uow.sent_scores.get_sent_scores_count(guild.id, player.id)
        unsent_scores = await self.storage_uow.sent_scores.get_unsent_scores_count(guild.id, player.id)

        # If there are not sent scores, then the player must be new to the system. Don't send scores
        if sent_scores == 0:
            return False

        # If there are more than 50 unsent scores then don't send.
        if unsent_scores > 50:
            return False

        return True
