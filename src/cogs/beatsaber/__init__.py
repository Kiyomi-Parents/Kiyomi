from sqlalchemy import create_engine

from .actions import Actions
from .beatsaber import BeatSaber
from .tasks import Tasks
from src.cogs.beatsaber.storage.database import Database
from src.cogs.beatsaber.storage.uow import UnitOfWork


def setup(bot):
    database = Database(create_engine("sqlite:///bot.db", echo=False))
    uow = UnitOfWork(bot, database)
    tasks = Tasks(uow)
    actions = Actions(uow, tasks)

    tasks.update_players.start()
    tasks.update_all_player_roles.start()
    tasks.update_players_scores.start()
    tasks.send_notifications.start()

    bot.add_cog(BeatSaber(uow, tasks, actions))
