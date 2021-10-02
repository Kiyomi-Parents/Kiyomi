from .actions import Actions
from .scoresaber import ScoreSaber
from .scoresaber_api import ScoreSaberAPI
from .storage.uow import UnitOfWork
from .tasks import Tasks
from src.kiyomi import Kiyomi


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot)
    score_saber_tasks = Tasks(uow)
    score_saber_actions = Actions(uow, score_saber_tasks)

    if not bot.running_tests:
        score_saber_tasks.update_players.start()
        score_saber_tasks.update_players_scores.start()

    bot.add_cog(ScoreSaber(uow, score_saber_tasks, score_saber_actions))
    bot.add_cog(ScoreSaberAPI(uow, score_saber_tasks, score_saber_actions))
