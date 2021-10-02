from typing import Optional, List

from ..model import MemberRole
from src.database import Repository


class MemberRoleRepository(Repository[MemberRole]):
    def get_by_id(self, entry_id: int) -> Optional[MemberRole]:
        return self._db.session.query(MemberRole) \
            .filter(MemberRole.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[MemberRole]]:
        return self._db.session.query(MemberRole) \
            .all()

    def get_by_guild_id_and_member_id_and_role_id(self, guild_id: int, member_id: int, role_id: int) -> Optional[MemberRole]:
        return self._db.session.query(MemberRole) \
            .filter(MemberRole.guild_id == guild_id) \
            .filter(MemberRole.member_id == member_id) \
            .filter(MemberRole.role_id == role_id) \
            .first()
