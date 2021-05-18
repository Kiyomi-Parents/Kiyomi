from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime

from src.storage.base import Base


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
    hash = Column(String, ForeignKey('score.songHash', ondelete="CASCADE"))
    uploaded = Column(String)
    directDownload = Column(String)
    downloadURL = Column(String)
    coverURL = Column(String)

    def __init__(self, songJson):
        if songJson is None:
            self._metadata = None
            self.stats = None
            self.description = None
            self.deletedAt = None
            self._id = None
            self.key = None
            self.name = None
            self.uploader = None
            self.hash = None
            self.uploaded = None
            self.directDownload = None
            self.downloadURL = None
            self.coverURL = None
        else:
            self._metadata = songJson["metadata"]
            self.stats = songJson["stats"]
            self.description = songJson["description"]
            self.deletedAt = songJson["deletedAt"]
            self._id = songJson["_id"]
            self.key = songJson["key"]
            self.name = songJson["name"]
            self.uploader = songJson["uploader"]
            self.hash = songJson["hash"]
            self.uploaded = songJson["uploaded"]
            self.directDownload = songJson["directDownload"]
            self.downloadURL = songJson["downloadURL"]
            self.coverURL = songJson["coverURL"]

    @property
    def beatsaver_url(self):
        return f"https://beatsaver.com/beatmap/{self.key}"

    @property
    def preview_url(self):
        return f"https://skystudioapps.com/bs-viewer/?id={self.key}"

    def __str__(self):
        return f"Song {self.name} ({self.key})"
