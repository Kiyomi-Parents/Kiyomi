from .actions import Actions
from .score_feed import ScoreFeed
from .storage.uow import UnitOfWork
from .tasks import Tasks
from src.kiyomi import Kiyomi


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot)
    score_feed_tasks = Tasks(uow)
    score_feed_actions = Actions(uow, score_feed_tasks)

    if not bot.running_tests:
        score_feed_tasks.send_notifications.start()

    bot.add_cog(ScoreFeed(uow, score_feed_actions))
