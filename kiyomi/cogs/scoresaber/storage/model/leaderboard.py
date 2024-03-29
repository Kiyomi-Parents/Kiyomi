from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

import pyscoresaber
from pyscoresaber import BeatmapDifficulty
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum, Float
from sqlalchemy.orm import relationship

from kiyomi.database import Base

if TYPE_CHECKING:
    from kiyomi.cogs.beatsaver.storage.model.beatmap_version_difficulty import (
        BeatmapVersionDifficulty,
    )


class Leaderboard(Base):
    """Leaderboard data from ScoreSaber"""

    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True)
    song_hash = Column(String(128))
    song_name = Column(String(128))
    song_sub_name = Column(String(128))
    song_author_name = Column(String(128))
    level_author_name = Column(String(128))
    max_score = Column(Integer)
    ranked = Column(Boolean)
    qualified = Column(Boolean)
    loved = Column(Boolean)
    stars = Column(Float)
    positive_modifiers = Column(Boolean)
    plays = Column(Integer)
    daily_plays = Column(Integer)
    cover_image = Column(String(256))
    max_pp = Column(Float)
    created_date = Column(DateTime(timezone=True))
    ranked_date = Column(DateTime(timezone=True))
    qualified_date = Column(DateTime(timezone=True))
    loved_date = Column(DateTime(timezone=True))

    difficulty_raw = Column(String(64))
    game_mode = Column(Enum(pyscoresaber.GameMode))
    difficulty = Column(Enum(pyscoresaber.BeatmapDifficulty))

    beatmap_version = relationship(
        "BeatmapVersion",
        primaryjoin="BeatmapVersion.hash == Leaderboard.song_hash",
        foreign_keys=[song_hash],
        uselist=False,
        lazy="selectin"
    )

    cached_at = Column(DateTime(timezone=True), nullable=False)

    def __init__(self, leaderboard: pyscoresaber.LeaderboardInfo):
        self.id = leaderboard.id
        self.song_hash = leaderboard.song_hash.lower()
        self.song_name = leaderboard.song_name
        self.song_sub_name = leaderboard.song_sub_name
        self.song_author_name = leaderboard.song_author_name
        self.level_author_name = leaderboard.level_author_name
        self.max_score = leaderboard.max_score
        self.ranked = leaderboard.ranked
        self.qualified = leaderboard.qualified
        self.loved = leaderboard.loved
        self.stars = leaderboard.stars
        self.positive_modifiers = leaderboard.positive_modifiers
        self.plays = leaderboard.plays
        self.daily_plays = leaderboard.daily_plays
        self.cover_image = leaderboard.cover_image
        self.max_pp = leaderboard.max_pp
        self.created_date = leaderboard.created_date
        self.ranked_date = leaderboard.ranked_date
        self.qualified_date = leaderboard.qualified_date
        self.loved_date = leaderboard.loved_date

        self.difficulty_raw = leaderboard.difficulty.difficulty_raw
        self.game_mode = leaderboard.difficulty.game_mode
        self.difficulty = leaderboard.difficulty.difficulty

        self.cached_at = datetime.utcnow()

    @property
    def song_name_full(self):
        if self.song_sub_name:
            return f"{self.song_name}: {self.song_sub_name}"

        return self.song_name

    @property
    def difficulty_name(self) -> str:
        difficulties = {
            BeatmapDifficulty.EASY: "Easy",
            BeatmapDifficulty.NORMAL: "Normal",
            BeatmapDifficulty.HARD: "Hard",
            BeatmapDifficulty.EXPERT: "Expert",
            BeatmapDifficulty.EXPERT_PLUS: "Expert+",
        }

        return difficulties[self.difficulty]

    @property
    def beatmap_difficulty(self) -> Optional["BeatmapVersionDifficulty"]:
        if self.beatmap_version is None:
            return None

        for beatmap_difficulty in self.beatmap_version.difficulties:
            if beatmap_difficulty.scoresaber_characteristic is not self.game_mode:
                continue

            if beatmap_difficulty.scoresaber_difficulty is not self.difficulty:
                continue

            return beatmap_difficulty

        return None

    @property
    def leaderboard_url(self) -> str:
        return f"https://scoresaber.com/leaderboard/{self.id}"

    def __str__(self):
        return f"Leaderboard {self.song_name} ({self.id})"
