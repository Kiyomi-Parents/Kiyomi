from typing import Optional, List

from ..model import Member
from src.database import Repository


class MemberRepository(Repository[Member]):
    def get_by_id(self, entry_id: int) -> Optional[Member]:
        return self._db.session.query(Member) \
            .filter(Member.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[Member]]:
        return self._db.session.query(Member) \
            .all()
