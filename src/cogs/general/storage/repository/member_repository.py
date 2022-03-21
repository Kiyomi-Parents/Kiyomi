from typing import Optional, List

from sqlalchemy.orm import Query

from ..model import Member
from src.database import BaseRepository


class MemberRepository(BaseRepository[Member]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Member) \
            .filter(Member.id == entry_id)

    def get_all(self) -> Optional[List[Member]]:
        return self.session.query(Member) \
            .all()
