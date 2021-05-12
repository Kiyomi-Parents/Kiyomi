from src.storage.model.song import Song


class SongRepository:
    def __init__(self, database):
        self._db = database

    def get_song_by_hash(self, songHash):
        return self._db.session.query(Song).filter(Song.hash == songHash).first()
