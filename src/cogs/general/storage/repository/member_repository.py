from typing import Type

from ..model.member import Member
from src.kiyomi.database import BaseRepository


class MemberRepository(BaseRepository[Member]):
    @property
    def _table(self) -> Type[Member]:
        return Member
