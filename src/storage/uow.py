from src.api import *
from src.storage.repository import *


class UnitOfWork:

    def __init__(self, bot, database):
        self.db = database

        self.guild_repo = GuildRepository(self.db)
        self.role_repo = RoleRepository(self.db)
        self.player_repo = PlayerRepository(self.db)
        self.score_repo = ScoreRepository(self.db)
        self.song_repo = SongRepository(self.db)

        self.scoresaber = ScoreSaber()
        self.beatsaver = BeatSaver()

        self.bot = bot
