from typing import Optional, List

from sqlalchemy.orm import Query

from ..model import Emoji
from src.database import BaseRepository


class EmojiRepository(BaseRepository[Emoji]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Emoji) \
            .filter(Emoji.id == entry_id)

    def get_all(self) -> Optional[List[Emoji]]:
        return self.session.query(Emoji) \
            .all()

    def get_by_name(self, emoji_name: str) -> Optional[Emoji]:
        return self.session.query(Emoji) \
            .filter(Emoji.name == emoji_name) \
            .first()

    def get_by_guild_id(self, guild_id: int) -> List[Emoji]:
        return self.session.query(Emoji) \
            .filter(Emoji.guild_id == guild_id) \
            .all()
