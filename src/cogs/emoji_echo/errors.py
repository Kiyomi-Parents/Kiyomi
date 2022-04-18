from typing import Optional

from src.kiyomi.error import CogException


class EmojiEchoCogException(CogException):
    pass


class NotFound(EmojiEchoCogException):
    def __init__(self, emoji_id: Optional[int] = None):
        self.emoji_id = emoji_id

    def __str__(self):
        return f"Could not find emoji with ID {self.emoji_id}"


class AlreadyEnabled(EmojiEchoCogException):
    pass
