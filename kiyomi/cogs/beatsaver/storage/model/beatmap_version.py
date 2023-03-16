from datetime import datetime

import pybeatsaver
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from kiyomi.database import Base
from .beatmap_version_difficulty import BeatmapVersionDifficulty


class BeatmapVersion(Base):
    """Map version data from BeatSaver"""

    __tablename__ = "beatmap_version"

    hash = Column(String(128), primary_key=True, autoincrement=False)
    map_id = Column(String(128), ForeignKey("beatmap.id", ondelete="CASCADE"))

    key = Column(String(128))
    state = Column(String(128))
    created_at = Column(DateTime(timezone=True))
    sage_score = Column(Integer)
    download_url = Column(String(256))
    cover_url = Column(String(256))
    preview_url = Column(String(256))

    difficulties = relationship("BeatmapVersionDifficulty", cascade="all, delete-orphan", lazy="selectin")

    beatmap = relationship("Beatmap", uselist=False, back_populates="versions", lazy="selectin")

    cached_at = Column(DateTime(timezone=True), nullable=False)

    def __init__(self, map_version: pybeatsaver.MapVersion):
        self.hash = map_version.hash.lower()
        self.key = map_version.key
        self.state = map_version.state.value
        self.created_at = map_version.created_at
        self.sage_score = map_version.sage_score
        self.download_url = map_version.download_url
        self.cover_url = map_version.cover_url
        self.preview_url = map_version.preview_url

        self.difficulties = []

        for version_diff in map_version.diffs:
            self.difficulties.append(BeatmapVersionDifficulty(version_diff))

        self.cached_at = datetime.utcnow()