from typing import Optional, List

from sqlalchemy.orm import Query

from ..model.member_role import MemberRole
from src.kiyomi.database import BaseRepository


class MemberRoleRepository(BaseRepository[MemberRole]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(MemberRole) \
            .filter(MemberRole.id == entry_id)

    def get_all(self) -> Optional[List[MemberRole]]:
        return self.session.query(MemberRole) \
            .all()

    def get_by_guild_id_and_member_id_and_role_id(self, guild_id: int, member_id: int, role_id: int) -> Optional[MemberRole]:
        return self.session.query(MemberRole) \
            .filter(MemberRole.guild_id == guild_id) \
            .filter(MemberRole.member_id == member_id) \
            .filter(MemberRole.role_id == role_id) \
            .first()
