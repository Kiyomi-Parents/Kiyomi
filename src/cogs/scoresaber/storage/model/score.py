from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pyscoresaber
from dateutil import tz
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

from src.kiyomi.database import Base

if TYPE_CHECKING:
    from src.cogs.beatsaver.storage.model.beatmap import Beatmap
    from src.cogs.beatsaver.storage.model.beatmap_version import BeatmapVersion


class Score(Base):
    """Score data from ScoreSaber"""

    __tablename__ = "score"

    id = Column(Integer, primary_key=True)

    # ScoreSaber info
    score_id = Column(Integer)
    rank = Column(Integer)
    base_score = Column(Integer)
    modified_score = Column(Integer)
    pp = Column(Float)
    weight = Column(Float)
    modifiers = Column(String(128))
    multiplier = Column(String(128))
    bad_cuts = Column(Integer)
    missed_notes = Column(Integer)
    max_combo = Column(Integer)
    full_combo = Column(Boolean)
    hmd = Column(Integer)
    has_replay = Column(Boolean)
    time_set = Column(DateTime(timezone=True))

    leaderboard_id = Column(Integer, ForeignKey("leaderboard.id", ondelete="CASCADE"))
    leaderboard = relationship("Leaderboard", uselist=False)

    player_id = Column(String(128), ForeignKey("player.id", ondelete="CASCADE"))
    player = relationship("Player", uselist=False, back_populates="scores")

    def __init__(self, player_score: pyscoresaber.PlayerScore):
        self.score_id = player_score.score.id
        self.rank = player_score.score.rank
        self.base_score = player_score.score.base_score
        self.modified_score = player_score.score.modified_score
        self.pp = player_score.score.pp
        self.weight = player_score.score.weight
        self.modifiers = player_score.score.modifiers
        self.multiplier = player_score.score.multiplier
        self.bad_cuts = player_score.score.bad_cuts
        self.missed_notes = player_score.score.missed_notes
        self.max_combo = player_score.score.max_combo
        self.full_combo = player_score.score.full_combo
        self.hmd = player_score.score.hmd
        self.has_replay = player_score.score.has_replay
        self.time_set = player_score.score.time_set

        self.leaderboard_id = player_score.leaderboard.id

        if player_score.score.leaderboard_player_info is not None:
            self.player_id = player_score.score.leaderboard_player_info.id

    @property
    def leaderboard_url(self):
        page = (self.rank - 1) // 12 + 1
        return f"https://scoresaber.com/leaderboard/{self.leaderboard_id}?page={page}"

    @property
    def accuracy(self) -> Optional[float]:
        max_score = self.leaderboard.max_score

        if not max_score and self.beatmap_version is not None:
            beatmap_difficulty = self.leaderboard.beatmap_difficulty

            if beatmap_difficulty is not None:
                max_score = beatmap_difficulty.max_score

        if max_score:
            return round(self.base_score / max_score * 100, 2)

        return None

    @property
    def weighted_pp(self) -> float:
        return round(self.pp * self.weight, 2)

    @property
    def beatmap_version(self) -> Optional[BeatmapVersion]:
        return self.leaderboard.beatmap_version

    @property
    def beatmap(self) -> Optional[Beatmap]:
        if self.beatmap_version is None:
            return None

        return self.beatmap_version.beatmap

    @property
    def get_hmd_name(self):
        if self.hmd == 0:
            return "Unknown"
        elif self.hmd == 1:
            return "Oculus Rift CV1"
        elif self.hmd == 2:
            return "HTC Vive"
        elif self.hmd == 4:
            return "HTC Vive Pro"
        elif self.hmd == 8:
            return "Windows Mixed Reality"
        elif self.hmd == 16:
            return "Oculus Rift S"
        elif self.hmd == 32:
            return "Oculus Quest"
        elif self.hmd == 64:
            return "Valve Index"
        elif self.hmd == 128:
            return "HTC Vive Cosmos"

        return "Unknown"

    @property
    def get_date(self):
        return self.time_set.replace(tzinfo=tz.UTC)

    def __str__(self):
        return f"Score {self.score_id} ({self.id})"
