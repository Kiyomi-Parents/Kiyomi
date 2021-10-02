from typing import Optional, List

from src.database import Repository
from ..model import Channel


class ChannelRepository(Repository[Channel]):
    def get_by_id(self, entry_id: int) -> Optional[Channel]:
        return self._db.session.query(Channel) \
            .filter(Channel.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[Channel]]:
        return self._db.session.query(Channel) \
            .all()
