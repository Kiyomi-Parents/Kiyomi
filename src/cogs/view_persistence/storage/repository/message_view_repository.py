from typing import Optional, List

from sqlalchemy.orm import Query

from src.cogs.view_persistence.storage.model.message_view import MessageView
from src.kiyomi import BaseRepository


class MessageViewRepository(BaseRepository[MessageView]):

    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(MessageView) \
            .filter(MessageView.id == entry_id)

    def get_all(self) -> Optional[List[MessageView]]:
        return self.session.query(MessageView).all()

    def get_by_message_id(self, message_id: int) -> MessageView:
        return self.session.query(MessageView) \
            .filter(MessageView.message_id == message_id) \
            .first()
