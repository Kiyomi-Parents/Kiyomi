from pyscoresaber import ScoreSaber

from Kiyomi import Kiyomi
from src.cogs.scoresaber.storage.repository.guild_player_repository import GuildPlayerRepository
from src.cogs.scoresaber.storage.repository.player_repository import PlayerRepository
from src.cogs.scoresaber.storage.repository.score_repository import ScoreRepository


class UnitOfWork:

    def __init__(self, bot: Kiyomi, scoresaber: ScoreSaber = None):
        self.player_repo = PlayerRepository(bot.database)
        self.score_repo = ScoreRepository(bot.database)
        self.guild_player_repo = GuildPlayerRepository(bot.database)

        if scoresaber is None:
            self.scoresaber = ScoreSaber()
        else:
            self.scoresaber = scoresaber

        self.bot = bot
