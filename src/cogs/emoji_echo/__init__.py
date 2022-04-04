from .emoji_echo import EmojiEcho
from .services.emoji_autocomplete_service import EmojiAutocompleteService
from .services.emoji_service import EmojiService
from .storage.unit_of_work import UnitOfWork
from src.kiyomi import Kiyomi


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    emoji_service = EmojiService(bot, uow)
    emoji_autocomplete_service = EmojiAutocompleteService(bot, uow)

    bot.add_cog(EmojiEcho(bot, emoji_service, emoji_autocomplete_service))
