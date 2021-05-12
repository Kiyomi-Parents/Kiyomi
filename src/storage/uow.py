from src.beatsaver import BeatSaver
from src.scoresaber import ScoreSaber
from src.storage.database import Database
from src.storage.repository.guild_repository import GuildRepository
from src.storage.repository.player_repository import PlayerRepository
from src.storage.repository.score_repository import ScoreRepository
from src.storage.repository.song_repository import SongRepository


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
