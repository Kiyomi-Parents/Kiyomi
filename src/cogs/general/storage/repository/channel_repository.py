from typing import Optional, List

from sqlalchemy.orm import Query

from src.database import BaseRepository
from ..model import Channel


class ChannelRepository(BaseRepository[Channel]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Channel) \
            .filter(Channel.id == entry_id)

    def get_all(self) -> Optional[List[Channel]]:
        return self.session.query(Channel) \
            .all()
