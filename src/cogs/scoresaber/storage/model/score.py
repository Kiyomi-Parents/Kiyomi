from typing import Optional

import pyscoresaber
from dateutil import tz
from pyscoresaber import Difficulty
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship

from src.cogs.scoresaber.scoresaber_utils import ScoreSaberUtils
from src.database import Base


class Score(Base):
    """Score data from ScoreSaber"""
    __tablename__ = "score"

    id = Column(Integer, primary_key=True)
    player_id = Column(String(128), ForeignKey("player.id", ondelete="CASCADE"))

    # ScoreSaber info
    rank = Column(Integer)
    score_id = Column(Integer)
    score = Column(Integer)
    unmodified_score = Column(Integer)
    mods = Column(String(128))
    pp = Column(Float)
    weight = Column(Float)
    time_set = Column(DateTime)
    leaderboard_id = Column(Integer)
    song_hash = Column(String(128))
    song_name = Column(String(128))
    song_sub_name = Column(String(128))
    song_author_name = Column(String(128))
    level_author_name = Column(String(128))
    characteristic = Column(Enum(pyscoresaber.Characteristic))
    difficulty = Column(Enum(pyscoresaber.Difficulty))
    max_score = Column(Integer)

    beatmap_version = relationship(
        "BeatmapVersion",
        primaryjoin='BeatmapVersion.hash == Score.song_hash',
        foreign_keys=[song_hash],
        uselist=False
    )

    def __init__(self, score_data: pyscoresaber.Score):
        self.rank = score_data.rank
        self.score_id = score_data.score_id
        self.score = score_data.score
        self.unmodified_score = score_data.unmodified_score
        self.mods = score_data.mods
        self.pp = score_data.pp
        self.weight = score_data.weight
        self.time_set = score_data.time_set
        self.leaderboard_id = score_data.leaderboard_id
        self.song_hash = score_data.song_hash.lower()
        self.song_name = score_data.song_name
        self.song_sub_name = score_data.song_sub_name
        self.song_author_name = score_data.song_author_name
        self.level_author_name = score_data.level_author_name
        self.characteristic = score_data.characteristic
        self.difficulty = score_data.difficulty
        self.max_score = score_data.max_score

    @property
    def leaderboard_url(self):
        page = (self.rank - 1) // 12 + 1
        return f"https://scoresaber.com/leaderboard/{self.leaderboard_id}?page={page}"

    @property
    def song_name_full(self):
        if self.song_sub_name:
            return f"{self.song_name}: {self.song_sub_name}"

        return self.song_name

    @property
    def difficulty_name(self) -> str:
        difficulties = {
            Difficulty.EASY: "Easy",
            Difficulty.NORMAL: "Normal",
            Difficulty.HARD: "Hard",
            Difficulty.EXPERT: "Expert",
            Difficulty.EXPERT_PLUS: "Expert+"
        }

        return difficulties[self.difficulty]

    @property
    def song_image_url(self) -> str:
        return f"https://scoresaber.com/imports/images/songs/{self.song_hash.upper()}.png"

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

    @property
    def weighted_pp(self) -> float:
        return round(self.pp * self.weight, 2)

    @property
    def get_date(self):
        return self.time_set.astimezone(tz.tzlocal())

    def __str__(self):
        return f"Score {self.song_name} ({self.score_id})"
