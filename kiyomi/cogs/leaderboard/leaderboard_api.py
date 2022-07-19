import pybeatsaver

from kiyomi import BaseCog
from .services import ServiceUnitOfWork
from .storage.models.guild_leaderboard import GuildLeaderboard


class LeaderboardAPI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    async def get_guild_leaderboard(
        self,
        guild_id: int,
        beatmap_hash: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> GuildLeaderboard:
        return await self._service_uow.score_leaderboards.get_guild_leaderboard(
            guild_id, beatmap_hash, characteristic, difficulty
        )
