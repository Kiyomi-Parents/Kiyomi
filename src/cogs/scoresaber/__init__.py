import pyscoresaber

from src.kiyomi import Kiyomi
from .arg_resolvers.player_id_resolver import PlayerIdResolver
from .scoresaber import ScoreSaber
from .scoresaber_api import ScoreSaberAPI
from .scoresaber_ui import ScoreSaberUI
from .services import PlayerService, ScoreService
from .storage import UnitOfWork
from .tasks import Tasks


def setup(bot: Kiyomi):
    scoresaber_api_client = pyscoresaber.ScoreSaberAPI(bot.loop)
    uow = UnitOfWork(bot.database.session)

    bot.error_resolver.add(PlayerIdResolver(uow))

    score_service = ScoreService(bot, uow, scoresaber_api_client)
    player_service = PlayerService(bot, uow, scoresaber_api_client, score_service)

    scoresaber_tasks = Tasks(bot, player_service, score_service)

    # Start listening to websocket
    bot.loop.create_task(scoresaber_tasks.init_live_score_feed())

    if not bot.running_tests:
        scoresaber_tasks.update_players.start()
        scoresaber_tasks.update_players_scores.start()

    bot.add_cog(ScoreSaber(bot, player_service, score_service))
    bot.add_cog(ScoreSaberAPI(bot, player_service, score_service, uow))
    bot.add_cog(ScoreSaberUI(bot, player_service, score_service))
