from typing import Optional, List

from src.database import Repository
from ..model import GuildMember


class GuildMemberRepository(Repository[GuildMember]):
    def get_by_id(self, entry_id: int) -> Optional[GuildMember]:
        return self._db.session.query(GuildMember) \
            .filter(GuildMember.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[GuildMember]]:
        return self._db.session.query(GuildMember) \
            .all()

    def get_all_by_guild_id(self, guild_id: int) -> Optional[List[GuildMember]]:
        return self._db.session.query(GuildMember) \
            .filter(GuildMember.guild_id == guild_id) \
            .all()

    def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildMember]:
        return self._db.session.query(GuildMember) \
            .filter(GuildMember.guild_id == guild_id) \
            .filter(GuildMember.member_id == member_id) \
            .first()
