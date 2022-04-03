from typing import Optional, List

from sqlalchemy.orm import Query

from ..model.message import Message
from src.kiyomi.database import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Message) \
            .filter(Message.id == entry_id)

    def get_all(self) -> Optional[List[Message]]:
        return self.session.query(Message) \
            .all()

    def get_by_channel_id(self, channel_id: int) -> List[Message]:
        return self.session.query(Message) \
            .filter(Message.channel_id == channel_id) \
            .all()
