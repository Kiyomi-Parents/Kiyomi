from .actions import Actions
from .beatsaver import BeatSaver
from .beatsaver_api import BeatSaverAPI
from .storage.uow import UnitOfWork


def setup(bot):
    uow = UnitOfWork(bot)
    beat_saver_actions = Actions(uow)

    bot.add_cog(BeatSaver(uow, beat_saver_actions))
    bot.add_cog(BeatSaverAPI(uow, beat_saver_actions))
