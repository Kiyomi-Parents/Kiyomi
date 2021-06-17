from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime

from src.storage.database import Base


class Song(Base):
    """Song data from BeatSaver"""
    __tablename__ = "song"

    id = Column(Integer, primary_key=True)

    # BeatSaver info
    _metadata = Column(JSON)
    stats = Column(JSON)
    description = Column(String)
    deletedAt = Column(DateTime)
    _id = Column(String)
    key = Column(String)
    name = Column(String)
    uploader = Column(JSON)
    hash = Column(String, ForeignKey("score.songHash", ondelete="CASCADE"))
    uploaded = Column(String)
    directDownload = Column(String)
    downloadURL = Column(String)
    coverURL = Column(String)

    def __init__(self, song_json):
        self._metadata = song_json["metadata"]
        self.stats = song_json["stats"]
        self.description = song_json["description"]
        self.deletedAt = song_json["deletedAt"]
        self._id = song_json["_id"]
        self.key = song_json["key"]
        self.name = song_json["name"]
        self.uploader = song_json["uploader"]
        self.hash = song_json["hash"]
        self.uploaded = song_json["uploaded"]
        self.directDownload = song_json["directDownload"]
        self.downloadURL = song_json["downloadURL"]
        self.coverURL = song_json["coverURL"]

    @property
    def beatsaver_url(self):
        return f"https://beatsaver.com/beatmap/{self.key}"

    @property
    def preview_url(self):
        return f"https://skystudioapps.com/bs-viewer/?id={self.key}"

    def __str__(self):
        return f"Song {self.name} ({self.key})"
