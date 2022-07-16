from typing import Type

from ..model.member import Member
from kiyomi.database import BaseStorageRepository


class MemberRepository(BaseStorageRepository[Member]):
    @property
    def _table(self) -> Type[Member]:
        return Member
