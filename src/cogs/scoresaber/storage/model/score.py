from typing import Optional

import pyscoresaber
from dateutil import tz
from pyscoresaber import Difficulty
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Enum, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class Score(Base):
    """Score data from ScoreSaber"""
    __tablename__ = "score"

    id = Column(Integer, primary_key=True)
    player_id = Column(String(128), ForeignKey("player.id", ondelete="CASCADE"))

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
    has_replay = Column(Boolean)
    time_set = Column(DateTime)

    leaderboard_id = Column(Integer, ForeignKey("leaderboard.id"))
    leaderboard = relationship(
        "Leaderboard",
        uselist=False
    )

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
        self.has_replay = player_score.score.has_replay
        self.time_set = player_score.score.time_set

        self.leaderboard_id = player_score.leaderboard.id

    # TODO: Probably broken
    @property
    def accuracy(self) -> Optional[float]:
        max_score = self.max_score

        if self.beatmap_version is not None:
            if not max_score and self.beatmap_version.beatmap is not None:
                for diff in self.beatmap_version.difficulties:
                    if diff.scoresaber_difficulty == self.difficulty and diff.scoresaber_characteristic == self.characteristic:
                        max_score = diff.max_score

        if max_score:
            return round(self.score / max_score * 100, 2)

        return None

    # TODO: Probably broken
    @property
    def weighted_pp(self) -> float:
        return round(self.pp * self.weight, 2)

    @property
    def get_date(self):
        return self.time_set.astimezone(tz.tzlocal())

    def __str__(self):
        return f"Score {self.score_id} ({self.id})"
