from src.kiyomi import Kiyomi
from .score_feed import ScoreFeed
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork
from .tasks import Tasks


async def setup(bot: Kiyomi):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    score_feed_tasks = Tasks(bot, service_uow)

    if not bot.running_tests:
        score_feed_tasks.send_notifications.start()

    await bot.add_cog(ScoreFeed(bot, service_uow))
