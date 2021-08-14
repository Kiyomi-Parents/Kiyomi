from .settings import Settings
from .settings_api import SettingsAPI
from .storage.uow import UnitOfWork
from .actions import Actions


def setup(bot):
    uow = UnitOfWork(bot)
    setting_actions = Actions(uow)

    bot.add_cog(Settings(uow, setting_actions))
    bot.add_cog(SettingsAPI(uow, setting_actions))
