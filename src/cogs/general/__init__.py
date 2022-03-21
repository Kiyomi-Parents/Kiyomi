from .general import General
from .general_api import GeneralAPI
from .services import EmojiService, GuildService, MemberService, RoleService
from .storage import UnitOfWork
from ...kiyomi import Kiyomi


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    emoji_service = EmojiService(bot, uow)
    guild_service = GuildService(bot, uow)
    member_service = MemberService(bot, uow, guild_service)
    role_service = RoleService(bot, uow, guild_service, member_service)

    bot.add_cog(General(bot, emoji_service, guild_service, member_service, role_service))
    bot.add_cog(GeneralAPI(bot, emoji_service, guild_service, member_service, role_service, uow))
