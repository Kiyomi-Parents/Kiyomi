from .arg_resolvers import *
from .general import General
from .general_api import GeneralAPI
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork
from kiyomi.kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    bot.error_resolver.add(ChannelIdResolver(storage_uow))
    bot.error_resolver.add(EmojiIdResolver(storage_uow))
    bot.error_resolver.add(GuildIdResolver(storage_uow))
    bot.error_resolver.add(MemberIdResolver(storage_uow))
    bot.error_resolver.add(MessageIdResolver(storage_uow))
    bot.error_resolver.add(RoleIdResolver(storage_uow))

    await bot.add_cog(General(bot, service_uow))
    await bot.add_cog(GeneralAPI(bot, service_uow))
