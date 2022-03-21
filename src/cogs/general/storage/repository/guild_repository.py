from typing import Optional, List

from sqlalchemy.orm import Query

from ..model import Guild
from src.database import BaseRepository


class GuildRepository(BaseRepository[Guild]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Guild) \
            .filter(Guild.id == entry_id)

    def get_all(self) -> Optional[List[Guild]]:
        return self.session.query(Guild) \
            .all()
