from typing import Optional, List

from ..model import Guild
from src.database import Repository


class GuildRepository(Repository[Guild]):
    def get_by_id(self, entry_id: int) -> Optional[Guild]:
        return self._db.session.query(Guild) \
            .filter(Guild.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[Guild]]:
        return self._db.session.query(Guild) \
            .all()
