from typing import Optional, List

from ..model import Role
from src.database import Repository


class RoleRepository(Repository[Role]):
    def get_by_id(self, entry_id: int) -> Optional[Role]:
        return self._db.session.query(Role) \
            .filter(Role.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[Role]]:
        return self._db.session.query(Role) \
            .all()
