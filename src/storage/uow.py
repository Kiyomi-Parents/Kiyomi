from src.api import *
from src.storage.repository import *


class UnitOfWork:

    def __init__(self, bot, database, scoresaber=None, beatsaver=None):
        self.db = database

        self.guild_repo = GuildRepository(self.db)
        self.role_repo = RoleRepository(self.db)
        self.player_repo = PlayerRepository(self.db)
        self.score_repo = ScoreRepository(self.db)
        self.song_repo = SongRepository(self.db)

        if scoresaber is None:
            self.scoresaber = ScoreSaber()
        else:
            self.scoresaber = scoresaber

        if beatsaver is None:
            self.beatsaver = BeatSaver()
        else:
            self.beatsaver = beatsaver

        self.bot = bot
