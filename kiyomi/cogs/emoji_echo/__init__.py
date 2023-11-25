import sentry_sdk

from .emoji_echo import EmojiEcho
from .emoji_echo_api import EmojiEchoAPI
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork
from kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    with sentry_sdk.start_transaction(name="Emoji Echo"):
        storage_uow = StorageUnitOfWork(bot.database.session)
        service_uow = ServiceUnitOfWork(bot, storage_uow)

        await bot.add_cog(EmojiEcho(bot, service_uow))
        await bot.add_cog(EmojiEchoAPI(bot, service_uow))
