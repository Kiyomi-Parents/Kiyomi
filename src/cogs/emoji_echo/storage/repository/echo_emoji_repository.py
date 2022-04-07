from typing import Optional, List

from sqlalchemy.orm import Query

from src.cogs.emoji_echo.storage.model.echo_emoji import EchoEmoji
from src.kiyomi import BaseRepository


class EchoEmojiRepository(BaseRepository[EchoEmoji]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(EchoEmoji) \
            .filter(EchoEmoji.id == entry_id)

    def get_all(self) -> Optional[List[EchoEmoji]]:
        return self.session.query(EchoEmoji) \
            .all()

    def get_by_emoji_id(self, emoji_id: int) -> Optional[EchoEmoji]:
        return self.session.query(EchoEmoji) \
            .filter(EchoEmoji.emoji_id == emoji_id) \
            .first()

    def get_by_guild_id(self, guild_id: int) -> Optional[List[EchoEmoji]]:
        return self.session.query(EchoEmoji) \
            .filter(EchoEmoji.guild_id == guild_id) \
            .all()

    def get_by_guild_id_and_emoji_id(self, guild_id: int, emoji_id: int) -> Optional[EchoEmoji]:
        return self.session.query(EchoEmoji) \
            .filter(EchoEmoji.guild_id == guild_id) \
            .filter(EchoEmoji.emoji_id == emoji_id) \
            .first()
