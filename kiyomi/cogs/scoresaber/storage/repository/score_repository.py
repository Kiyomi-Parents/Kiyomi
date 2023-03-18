from datetime import datetime
from typing import Optional, List, Type

from sqlalchemy import select, desc, exists, func
from sqlalchemy.orm import selectinload, raiseload

from kiyomi.cogs.beatsaver.storage.model.beatmap_version import BeatmapVersion
from kiyomi.database import BaseStorageRepository
from ..model.leaderboard import Leaderboard
from ..model.player import Player
from ..model.score import Score


class ScoreRepository(BaseStorageRepository[Score]):
    @property
    def _table(self) -> Type[Score]:
        return Score

    async def get_by_score_id(self, score_id: int) -> Optional[Score]:
        stmt = select(self._table).where(self._table.score_id == score_id)
        return await self._first(stmt)

    async def get_all_by_player_id_and_leaderboard_id(self, player_id: str, leaderboard_id: int) -> List[Score]:
        stmt = (
            select(self._table)
            .where(self._table.player_id == player_id)
            .where(self._table.leaderboard_id == leaderboard_id)
            .options(
                    selectinload(self._table.player),
                    selectinload(self._table.player).raiseload(Player.guild_players),
                    selectinload(self._table.player).raiseload(Player.scores),
                    raiseload(self._table.leaderboard)
            )
        )
        return await self._all(stmt)

    async def get_best_score_by_player_id_and_leaderboard_id(self, player_id: str, leaderboard_id: int) -> Optional[Score]:
        stmt = (
            select(self._table)
            .where(self._table.player_id == player_id)
            .where(self._table.leaderboard_id == leaderboard_id)
            .order_by(self._table.modified_score.desc())
            .limit(1)
            .options(
                    selectinload(self._table.player),
                    selectinload(self._table.player).raiseload(Player.guild_players),
                    selectinload(self._table.player).raiseload(Player.scores),

                    selectinload(self._table.leaderboard),

                    selectinload(self._table.leaderboard)
                    .selectinload(Leaderboard.beatmap_version),

                    selectinload(self._table.leaderboard)
                    .selectinload(Leaderboard.beatmap_version)
                    .raiseload(BeatmapVersion.beatmap),

                    selectinload(self._table.leaderboard)
                    .selectinload(Leaderboard.beatmap_version)
                    .selectinload(BeatmapVersion.difficulties)
            )
        )
        return await self._first(stmt)

    async def get_previous(self, score: Score) -> Optional[Score]:
        stmt = (
            select(self._table)
            .where(self._table.score_id == score.score_id)
            .where(self._table.time_set < score.time_set)
            .order_by(desc(self._table.time_set))
            .limit(1)
        )
        return await self._first(stmt)

    async def get_recent(self, player_id: str, count: int) -> List[Score]:
        stmt = (
            select(self._table).where(self._table.player_id == player_id).order_by(desc(self._table.time_set)).limit(count)
        )
        return await self._all(stmt)

    async def exists_by_score_id_and_time_set(self, score_id: int, time_set: datetime) -> bool:
        stmt = select(self._table).where(self._table.score_id == score_id).where(self._table.time_set == time_set)
        stmt = exists(stmt).select()
        result = await self._execute_scalars(stmt)
        return result.one()

    async def get_all_sorted_by_pp(self, player_id: str) -> List[Score]:
        latest_scores = (
            select(self._table.id, self._table.score_id, func.max(self._table.time_set))
            .where(self._table.player_id == player_id)
            .group_by(self._table.score_id)
        )

        stmt = (
            select(self._table)
            .where(self._table.id.in_(latest_scores.select(self._table.id)))
            .order_by(desc(self._table.pp))
         )

        return await self._all(stmt)
