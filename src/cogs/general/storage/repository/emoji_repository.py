from typing import Optional, List

from ..model import Emoji
from src.database import Repository


class EmojiRepository(Repository[Emoji]):
    def get_by_id(self, entry_id: int) -> Optional[Emoji]:
        return self._db.session.query(Emoji) \
            .filter(Emoji.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[Emoji]]:
        return self._db.session.query(Emoji) \
            .all()

    def get_by_name(self, emoji_name: str) -> Optional[Emoji]:
        return self._db.session.query(Emoji) \
            .filter(Emoji.name == emoji_name) \
            .first()
