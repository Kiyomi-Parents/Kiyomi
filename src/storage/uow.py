from src.storage.repository import *
from src.api import ScoreSaber, BeatSaver


class UnitOfWork:

    def __init__(self, bot, database, scoresaber=None, beatsaver=None):
        self.database = database

        self.guild_repo = GuildRepository(self.database)
        self.role_repo = RoleRepository(self.database)
        self.player_repo = PlayerRepository(self.database)
        self.score_repo = ScoreRepository(self.database)
        self.song_repo = SongRepository(self.database)

        if scoresaber is None:
            self.scoresaber = ScoreSaber()
        else:
            self.scoresaber = scoresaber

        if beatsaver is None:
            self.beatsaver = BeatSaver()
        else:
            self.beatsaver = beatsaver

        self.bot = bot
