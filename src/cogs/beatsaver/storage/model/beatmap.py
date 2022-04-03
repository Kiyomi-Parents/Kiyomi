import time
from typing import List, Optional

from pybeatsaver import MapDetail
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship

from src.kiyomi.database import Base, EMapTagList
from .beatmap_version import BeatmapVersion
from .beatmap_version_difficulty import BeatmapVersionDifficulty


class Beatmap(Base):
    """Song data from BeatSaver"""
    __tablename__ = "beatmap"

    # BeatSaver info
    id = Column(String(128), primary_key=True, autoincrement=False)
    name = Column(String(256))
    description = Column(Text)
    uploaded = Column(DateTime)
    automapper = Column(Boolean)
    ranked = Column(Boolean)
    qualified = Column(Boolean)
    tags = Column(EMapTagList)

    # Uploader
    uploader_id = Column(Integer)
    uploader_name = Column(String(128))
    uploader_hash = Column(String(128))
    uploader_avatar = Column(String(128))

    # Map metadata
    metadata_bpm = Column(Float)
    metadata_duration = Column(Integer)
    metadata_song_name = Column(String(128))
    metadata_song_sub_name = Column(String(128))
    metadata_song_author_name = Column(String(128))
    metadata_level_author_name = Column(String(128))

    # Stats
    stats_plays = Column(Integer)
    stats_downloads = Column(Integer)
    stats_upvotes = Column(Integer)
    stats_downvotes = Column(Integer)
    stats_score = Column(Integer)

    versions = relationship("BeatmapVersion", back_populates="beatmap", cascade="all, delete-orphan")

    def __init__(self, map_detail: MapDetail):
        self.id = map_detail.id
        self.name = map_detail.name
        self.description = map_detail.description
        self.uploaded = map_detail.uploaded
        self.automapper = map_detail.automapper
        self.ranked = map_detail.ranked
        self.qualified = map_detail.qualified
        self.tags = map_detail.tags

        self.uploader_id = map_detail.uploader.id
        self.uploader_name = map_detail.uploader.name
        self.uploader_hash = map_detail.uploader.hash
        self.uploader_avatar = map_detail.uploader.avatar

        self.metadata_bpm = map_detail.metadata.bpm
        self.metadata_duration = map_detail.metadata.duration
        self.metadata_song_name = map_detail.metadata.song_name
        self.metadata_song_sub_name = map_detail.metadata.song_sub_name
        self.metadata_song_author_name = map_detail.metadata.song_author_name
        self.metadata_level_author_name = map_detail.metadata.level_author_name

        self.stats_plays = map_detail.stats.plays
        self.stats_downloads = map_detail.stats.downloads
        self.stats_upvotes = map_detail.stats.upvotes
        self.stats_downvotes = map_detail.stats.downvotes
        self.stats_score = map_detail.stats.score

        self.versions = []

        for map_version in map_detail.versions:
            self.versions.append(BeatmapVersion(map_version))

    @property
    def latest_version(self) -> Optional[BeatmapVersion]:
        latest = None

        for version in self.versions:
            if latest is None:
                latest = version
                continue

            if latest.created_at < version.created_at:
                latest = version

        return latest

    @property
    def beatsaver_url(self) -> str:
        return f"https://beatsaver.com/maps/{self.id}"

    @property
    def mapper_url(self) -> str:
        return f"https://beatsaver.com/profile/{self.uploader_id}"

    @property
    def preview_url(self) -> str:
        return f"https://skystudioapps.com/bs-viewer/?id={self.id}"

    @property
    def cover_url(self) -> str:
        return self.latest_version.cover_url

    @property
    def one_click_install(self) -> str:
        return f"beatsaver://{self.id}"

    @property
    def rating(self) -> float:
        return round(self.stats_score * 100, 1)

    @property
    def length(self) -> str:
        return time.strftime("%H:%M:%S", time.gmtime(self.metadata_duration))

    @property
    def difficulties(self) -> List[BeatmapVersionDifficulty]:
        return self.latest_version.difficulties

    def __str__(self):
        return f"Beatmap {self.name} ({self.id})"
