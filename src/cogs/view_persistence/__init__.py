from src.kiyomi import Kiyomi
from .services import MessageViewService
from .storage import UnitOfWork
from .view_persistance_api import ViewPersistenceAPI


async def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    message_view_service = MessageViewService(bot, uow)

    await bot.add_cog(ViewPersistenceAPI(bot, message_view_service, uow))
