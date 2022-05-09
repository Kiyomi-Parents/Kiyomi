from .services.emoji_service import EmojiService
from src.kiyomi import BaseCog, Kiyomi


class EmojiEchoCog(BaseCog):
    def __init__(self, bot: Kiyomi, emoji_service: EmojiService):
        super().__init__(bot)

        self.emoji_service = emoji_service
