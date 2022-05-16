from .arg_resolvers import *
from .general import General
from .general_api import GeneralAPI
from .services import EmojiService, GuildService, MemberService, RoleService, ChannelService, MessageService
from .storage import UnitOfWork
from ...kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    uow = UnitOfWork(await bot.database.get_session())

    bot.error_resolver.add(ChannelIdResolver(uow))
    bot.error_resolver.add(EmojiIdResolver(uow))
    bot.error_resolver.add(GuildIdResolver(uow))
    bot.error_resolver.add(MemberIdResolver(uow))
    bot.error_resolver.add(MessageIdResolver(uow))
    bot.error_resolver.add(RoleIdResolver(uow))

    guild_service = GuildService(bot, uow)
    emoji_service = EmojiService(bot, uow, guild_service)
    member_service = MemberService(bot, uow, guild_service)
    channel_service = ChannelService(bot, uow, guild_service)
    message_service = MessageService(bot, uow, guild_service, channel_service)
    role_service = RoleService(bot, uow, guild_service, member_service)

    await bot.add_cog(
            General(
                    bot,
                    emoji_service,
                    guild_service,
                    member_service,
                    channel_service,
                    message_service,
                    role_service
            )
    )
    await bot.add_cog(
            GeneralAPI(
                    bot,
                    emoji_service,
                    guild_service,
                    member_service,
                    channel_service,
                    message_service,
                    role_service,
                    uow
            )
    )
