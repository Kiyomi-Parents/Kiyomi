from src.api import *
from src.storage.database import Database
from src.storage.repository import *


class UnitOfWork:

    def __init__(self, client):
        self.db = Database()

        self.guild_repo = GuildRepository(self.db)
        self.player_repo = PlayerRepository(self.db)
        self.score_repo = ScoreRepository(self.db)
        self.song_repo = SongRepository(self.db)

        self.scoresaber = ScoreSaber()
        self.beatsaver = BeatSaver()

        self.client = client
