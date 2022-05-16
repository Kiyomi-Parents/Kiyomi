from src.kiyomi import Kiyomi
from .score_feed import ScoreFeed
from .services import NotificationService, SentScoreService
from .storage import UnitOfWork
from .tasks import Tasks


async def setup(bot: Kiyomi):
    uow = UnitOfWork(await bot.database.get_session())

    sent_score_service = SentScoreService(bot, uow)
    notification_service = NotificationService(bot, uow, sent_score_service)

    score_feed_tasks = Tasks(bot, notification_service)

    if not bot.running_tests:
        score_feed_tasks.send_notifications.start()

    await bot.add_cog(ScoreFeed(bot, notification_service, sent_score_service))
