from typing import Type

from ..model.role import Role
from kiyomi.database import BaseStorageRepository


class RoleRepository(BaseStorageRepository[Role]):
    @property
    def _table(self) -> Type[Role]:
        return Role
