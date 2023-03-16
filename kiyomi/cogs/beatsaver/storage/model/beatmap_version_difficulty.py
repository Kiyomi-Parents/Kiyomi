from datetime import datetime

import pybeatsaver.models.enum
import pyscoresaber.models.enum
from pybeatsaver import MapDifficulty
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship

from kiyomi.database import Base
from ...beatsaver_utils import BeatSaverUtils


class BeatmapVersionDifficulty(Base):
    """Map version difficulty data from BeatSaver"""

    __tablename__ = "beatmap_version_difficulty"

    id = Column(Integer, primary_key=True)
    version_hash = Column(String(128), ForeignKey("beatmap_version.hash", ondelete="CASCADE"))

    njs = Column(Float)
    offset = Column(Float)
    notes = Column(Integer)
    bombs = Column(Integer)
    obstacles = Column(Integer)
    nps = Column(Float)
    length = Column(Float)
    characteristic = Column(Enum(pybeatsaver.ECharacteristic))
    difficulty = Column(Enum(pybeatsaver.EDifficulty))
    events = Column(Integer)
    chroma = Column(Boolean)
    me = Column(Boolean)  # Mapping extensions
    ne = Column(Boolean)  # Noodle extensions
    cinema = Column(Boolean)
    seconds = Column(Float)
    stars = Column(Float)

    # Party summary
    parity_errors = Column(Integer)
    parity_warns = Column(Integer)
    parity_resets = Column(Integer)

    beatmap_version = relationship("BeatmapVersion", uselist=False, back_populates="difficulties", lazy="selectin")

    cached_at = Column(DateTime(timezone=True), nullable=False)

    def __init__(self, version_difficulty: MapDifficulty):
        self.njs = version_difficulty.njs
        self.offset = version_difficulty.offset
        self.notes = version_difficulty.notes
        self.bombs = version_difficulty.bombs
        self.obstacles = version_difficulty.obstacles
        self.nps = version_difficulty.nps
        self.length = version_difficulty.length
        self.characteristic = version_difficulty.characteristic
        self.difficulty = version_difficulty.difficulty
        self.events = version_difficulty.events
        self.chroma = version_difficulty.chroma
        self.me = version_difficulty.me
        self.ne = version_difficulty.ne
        self.cinema = version_difficulty.cinema
        self.seconds = version_difficulty.seconds
        self.stars = version_difficulty.stars

        self.parity_errors = version_difficulty.parity_summary.errors
        self.parity_warns = version_difficulty.parity_summary.warns
        self.parity_resets = version_difficulty.parity_summary.resets

        self.cached_at = datetime.utcnow()

    @property
    def max_score(self) -> Integer:
        return BeatSaverUtils.get_max_score(self.notes)

    @property
    def scoresaber_characteristic(self) -> pyscoresaber.GameMode:
        return BeatSaverUtils.to_scoresaber_game_mode(self.characteristic)

    @property
    def scoresaber_difficulty(self) -> pyscoresaber.BeatmapDifficulty:
        return BeatSaverUtils.to_scoresaber_difficulty(self.difficulty)

    @property
    def characteristic_text(self) -> str:
        return self.characteristic.human_readable

    @property
    def difficulty_text(self) -> str:
        return self.difficulty.human_readable

    def __str__(self) -> str:
        return f"Beatmap Version Difficulty {self.characteristic} {self.difficulty} ({self.id})"

    def __repr__(self) -> str:
        return self.__str__()
