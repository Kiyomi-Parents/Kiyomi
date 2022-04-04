from .services.emoji_service import EmojiService
from .services.emoji_autocomplete_service import EmojiAutocompleteService
from src.kiyomi import BaseCog, Kiyomi


class EmojiEchoCog(BaseCog):
    def __init__(self, bot: Kiyomi, emoji_service: EmojiService, emoji_autocomplete_service: EmojiAutocompleteService):
        super().__init__(bot)

        self.emoji_service = emoji_service
        self.emoji_autocomplete_service = emoji_autocomplete_service
