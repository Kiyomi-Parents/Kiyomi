from .actions import Actions
from .score_feed import ScoreFeed
from .storage.uow import UnitOfWork
from .tasks import Tasks


def setup(bot):
    uow = UnitOfWork(bot)
    score_feed_tasks = Tasks(uow)
    score_feed_actions = Actions(uow, score_feed_tasks)

    score_feed_tasks.send_notifications.start()

    bot.add_cog(ScoreFeed(uow, score_feed_actions))