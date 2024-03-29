import sentry_sdk

from kiyomi import Kiyomi
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork
from .view_persistance_api import ViewPersistenceAPI


async def setup(bot: Kiyomi):
    with sentry_sdk.start_transaction(name="View Persistence"):
        storage_uow = StorageUnitOfWork(bot.database.session)
        service_uow = ServiceUnitOfWork(bot, storage_uow)

        await bot.add_cog(ViewPersistenceAPI(bot, service_uow))
