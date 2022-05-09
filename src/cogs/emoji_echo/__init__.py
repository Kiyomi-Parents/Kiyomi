from .emoji_echo import EmojiEcho
from .emoji_echo_api import EmojiEchoAPI
from .services.emoji_service import EmojiService
from .storage.unit_of_work import UnitOfWork
from src.kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    emoji_service = EmojiService(bot, uow)

    await bot.add_cog(EmojiEcho(bot, emoji_service))
    await bot.add_cog(EmojiEchoAPI(bot, emoji_service, uow))
