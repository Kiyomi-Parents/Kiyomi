from src.storage.model.song import Song


class SongRepository:
    def __init__(self, database):
        self._db = database

    def get_songs(self):
        return self._db.session.query(Song).all()

    def get_song_by_hash(self, song_hash):
        return self._db.session.query(Song).filter(Song.hash == song_hash).first()
