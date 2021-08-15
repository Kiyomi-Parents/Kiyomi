import pybeatsaver.models.enum
import pyscoresaber.models.enum
from pybeatsaver import MapDifficulty
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Boolean, Enum

from ...beatsaver_utils import BeatSaverUtils
from src.database import Base


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
    characteristic = Column(Enum(pybeatsaver.Characteristic))
    difficulty = Column(Enum(pybeatsaver.Difficulty))
    events = Column(Integer)
    chroma = Column(Boolean)
    me = Column(Boolean)
    ne = Column(Boolean)
    cinema = Column(Boolean)
    seconds = Column(Float)

    # Party summary
    parity_errors = Column(Integer)
    parity_warns = Column(Integer)
    parity_resets = Column(Integer)

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
        self.parity_errors = version_difficulty.parity_summary.errors
        self.parity_warns = version_difficulty.parity_summary.warns
        self.parity_resets = version_difficulty.parity_summary.resets

    @property
    def max_score(self) -> Integer:
        return BeatSaverUtils.get_max_score(self.notes)

    @property
    def scoresaber_characteristic(self) -> pyscoresaber.Characteristic:
        characteristics = {
            pybeatsaver.Characteristic.STANDARD: pyscoresaber.Characteristic.STANDARD,
            pybeatsaver.Characteristic.ONE_SABER: pyscoresaber.Characteristic.ONE_SABER,
            pybeatsaver.Characteristic.NO_ARROWS: pyscoresaber.Characteristic.NO_ARROWS,
            pybeatsaver.Characteristic.DEGREE_90: pyscoresaber.Characteristic.DEGREE_90,
            pybeatsaver.Characteristic.DEGREE_360: pyscoresaber.Characteristic.DEGREE_360,
            pybeatsaver.Characteristic.LIGHTSHOW: pyscoresaber.Characteristic.LIGHTSHOW,
            pybeatsaver.Characteristic.LAWLESS: pyscoresaber.Characteristic.LAWLESS
        }

        return characteristics[self.characteristic]

    @property
    def scoresaber_difficulty(self) -> pyscoresaber.Difficulty:
        difficulties = {
            pybeatsaver.Difficulty.EASY: pyscoresaber.Difficulty.EASY,
            pybeatsaver.Difficulty.NORMAL: pyscoresaber.Difficulty.NORMAL,
            pybeatsaver.Difficulty.HARD: pyscoresaber.Difficulty.HARD,
            pybeatsaver.Difficulty.EXPERT: pyscoresaber.Difficulty.EXPERT,
            pybeatsaver.Difficulty.EXPERT_PLUS: pyscoresaber.Difficulty.EXPERT_PLUS
        }

        return difficulties[self.difficulty]
