import pyscoresaber

from src.kiyomi import Kiyomi
from .arg_resolvers import *
from .scoresaber import ScoreSaber
from .scoresaber_api import ScoreSaberAPI
from .scoresaber_ui import ScoreSaberUI
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork
from .tasks import Tasks


async def setup(bot: Kiyomi):
    scoresaber_api_client = pyscoresaber.ScoreSaberAPI(bot.loop)
    await scoresaber_api_client.start()
    await scoresaber_api_client.ws_start()

    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow, scoresaber_api_client)

    bot.error_resolver.add(PlayerIdResolver(storage_uow))

    scoresaber_tasks = Tasks(bot, service_uow)

    # Start listening to websocket
    bot.loop.create_task(scoresaber_tasks.init_live_score_feed())

    scoresaber_tasks.update_players.start()
    scoresaber_tasks.update_players_scores.start()

    await bot.add_cog(ScoreSaber(bot, service_uow))
    await bot.add_cog(ScoreSaberAPI(bot, service_uow))
    await bot.add_cog(ScoreSaberUI(bot, service_uow))
