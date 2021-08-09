import pybeatsaver
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from src.cogs.beatsaber.storage.database import Base
from src.cogs.beatsaber.storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty


class BeatmapVersion(Base):
    """Map version data from BeatSaver"""
    __tablename__ = "beatmap_version"

    hash = Column(String, ForeignKey("score.song_hash", ondelete="CASCADE"), primary_key=True)
    map_id = Column(Integer, ForeignKey("beatmap.id", ondelete="CASCADE"))

    key = Column(String)
    state = Column(String)
    created_at = Column(DateTime)
    sage_score = Column(Integer)
    download_url = Column(String)
    cover_url = Column(String)
    preview_url = Column(String)

    difficulties = relationship("BeatmapVersionDifficulty", cascade="all, delete-orphan")

    beatmap = relationship("Beatmap", back_populates="versions")

    def __init__(self, map_version: pybeatsaver.MapVersion):
        self.hash = map_version.hash
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
