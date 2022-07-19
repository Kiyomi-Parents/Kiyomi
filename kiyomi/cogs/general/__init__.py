from .arg_resolvers import *
from .general import General
from .general_api import GeneralAPI
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork
from kiyomi.kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    bot.error_resolver.add(ChannelIdResolver(service_uow))
    bot.error_resolver.add(EmojiIdResolver(service_uow))
    bot.error_resolver.add(GuildIdResolver(service_uow))
    bot.error_resolver.add(MemberIdResolver(service_uow))
    bot.error_resolver.add(MessageIdResolver(service_uow))
    bot.error_resolver.add(RoleIdResolver(service_uow))

    await bot.add_cog(General(bot, service_uow))
    await bot.add_cog(GeneralAPI(bot, service_uow))
