from typing import List, Optional

import pybeatsaver

from kiyomi.cogs.beatsaver import BeatSaverAPI
from kiyomi.cogs.beatsaver.beatsaver_utils import BeatSaverUtils
from kiyomi.cogs.scoresaber import ScoreSaberAPI
from kiyomi.cogs.scoresaber.storage.model.player import Player
from kiyomi.cogs.scoresaber.storage.model.score import Score
from ..storage import StorageUnitOfWork
from kiyomi.service.base_basic_service import BaseBasicService
from ..storage.models.guild_leaderboard import GuildLeaderboard
from ...scoresaber.storage.model.leaderboard import Leaderboard


class GuildLeaderboardService(BaseBasicService[StorageUnitOfWork]):
    async def get_guild_leaderboard_by_key(
        self,
        guild_id: int,
        beatmap_key: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> GuildLeaderboard:
        async with self.bot.get_cog_api(BeatSaverAPI) as beatsaver:
            beatmap_hash = await beatsaver.get_beatmap_hash_by_key(beatmap_key)

        if beatmap_hash is None:
            return GuildLeaderboard(None, [])

        return await self.get_guild_leaderboard(guild_id, beatmap_hash, characteristic, difficulty)

    async def get_guild_leaderboard(
        self,
        guild_id: int,
        beatmap_hash: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> GuildLeaderboard:
        async with self.bot.get_cog_api(ScoreSaberAPI) as scoresaber:
            leaderboard = await scoresaber.get_leaderboard(
                beatmap_hash,
                BeatSaverUtils.to_scoresaber_game_mode(characteristic),
                BeatSaverUtils.to_scoresaber_difficulty(difficulty),
            )

            if leaderboard is None:
                return GuildLeaderboard(None, [])

            guild_players = await scoresaber.get_guild_players_by_guild(guild_id)

        return await self._make_guild_leaderboard([guild_player.player for guild_player in guild_players], leaderboard)

    async def _make_guild_leaderboard(self, players: List[Player], leaderboard: Leaderboard) -> GuildLeaderboard:
        guild_leaderboard = GuildLeaderboard(leaderboard)

        async with self.bot.get_cog_api(ScoreSaberAPI) as scoresaber:
            for player in players:
                scores = await scoresaber.get_score_by_player_id_and_leaderboard_id(player.id, leaderboard.id)
                best_score = self.get_best_score(scores)

                if best_score is not None:
                    guild_leaderboard.add_score(best_score)

        return guild_leaderboard

    @staticmethod
    def get_best_score(scores: List[Score]) -> Optional[Score]:
        best_score = None

        for score in scores:
            if best_score is None:
                best_score = score
                continue

            # Not sure if modified_score is the best thing to use here
            if score.modified_score > best_score.modified_score:
                best_score = score

        return best_score
