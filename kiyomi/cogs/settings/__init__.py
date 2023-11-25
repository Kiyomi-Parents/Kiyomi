import sentry_sdk

from kiyomi import Kiyomi
from .services import ServiceUnitOfWork
from .settings import Settings
from .settings_api import SettingsAPI
from .storage import StorageUnitOfWork


async def setup(bot: Kiyomi):
    with sentry_sdk.start_transaction(name="Settings"):
        storage_uow = StorageUnitOfWork(bot.database.session)
        service_uow = ServiceUnitOfWork(bot, storage_uow)
    
        await bot.add_cog(Settings(bot, service_uow))
        await bot.add_cog(SettingsAPI(bot, service_uow))
