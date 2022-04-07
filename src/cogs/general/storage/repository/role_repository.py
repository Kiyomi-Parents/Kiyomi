from typing import Optional, List

from sqlalchemy.orm import Query

from ..model.role import Role
from src.kiyomi.database import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Role) \
            .filter(Role.id == entry_id)

    def get_all(self) -> Optional[List[Role]]:
        return self.session.query(Role) \
            .all()
