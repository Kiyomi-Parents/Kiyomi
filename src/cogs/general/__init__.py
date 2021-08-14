from .actions import Actions
from .general import General
from .general_api import GeneralAPI
from .storage.uow import UnitOfWork


def setup(bot):
    uow = UnitOfWork(bot)
    general_actions = Actions(uow)

    bot.add_cog(General(uow, general_actions))
    bot.add_cog(GeneralAPI(uow, general_actions))
