from src.cogs.beatsaber.api.beatsaver import BeatSaver
from src.cogs.beatsaber.api.scoresaber import ScoreSaber
from src.cogs.beatsaber.storage.repository.guild_repository import GuildRepository
from src.cogs.beatsaber.storage.repository.player_repository import PlayerRepository
from src.cogs.beatsaber.storage.repository.role_repository import RoleRepository
from src.cogs.beatsaber.storage.repository.score_repository import ScoreRepository
from src.cogs.beatsaber.storage.repository.song_repository import SongRepository


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
