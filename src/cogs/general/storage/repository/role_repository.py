from typing import Type

from ..model.role import Role
from src.kiyomi.database import BaseRepository


class RoleRepository(BaseRepository[Role]):
    @property
    def _table(self) -> Type[Role]:
        return Role
