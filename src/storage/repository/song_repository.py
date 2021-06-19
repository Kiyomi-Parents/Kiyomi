from src.storage.model.song import Song


class SongRepository:
    def __init__(self, database):
        self._db = database

    def get_songs(self):
        return self._db.session.query(Song).all()

    def get_song_by_hash(self, song_hash):
        return self._db.session.query(Song).filter(Song.hash == song_hash).first()

    def get_song_by_key(self, song_key):
        return self._db.session.query(Song).filter(Song.key == song_key).first()

    def add_song(self, db_song):
        self._db.add_entry(db_song)

        return self.get_song_by_key(db_song.key)
