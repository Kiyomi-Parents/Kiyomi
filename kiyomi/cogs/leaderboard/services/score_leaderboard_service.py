from typing import List

import pybeatsaver

from kiyomi.cogs.beatsaver import BeatSaverAPI
from kiyomi.cogs.beatsaver.beatsaver_utils import BeatSaverUtils
from kiyomi.cogs.scoresaber import ScoreSaberAPI
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

            player_ids = await scoresaber.get_player_ids_by_guild(guild_id)

        return await self._make_guild_leaderboard(player_ids, leaderboard)

    async def _make_guild_leaderboard(self, player_ids: List[int], leaderboard: Leaderboard) -> GuildLeaderboard:
        guild_leaderboard = GuildLeaderboard(leaderboard)

        async with self.bot.get_cog_api(ScoreSaberAPI) as scoresaber:
            for player_id in player_ids:
                best_score = await scoresaber.get_best_score_by_player_id_and_leaderboard_id(player_id, leaderboard.id)

                if best_score is not None:
                    guild_leaderboard.add_score(best_score)

        return guild_leaderboard

