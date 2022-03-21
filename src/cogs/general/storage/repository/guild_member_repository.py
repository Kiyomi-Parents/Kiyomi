from typing import Optional, List

from sqlalchemy.orm import Query

from src.database import BaseRepository
from ..model import GuildMember


class GuildMemberRepository(BaseRepository[GuildMember]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(GuildMember) \
            .filter(GuildMember.id == entry_id)

    def get_all(self) -> Optional[List[GuildMember]]:
        return self.session.query(GuildMember) \
            .all()

    def get_all_by_guild_id(self, guild_id: int) -> Optional[List[GuildMember]]:
        return self.session.query(GuildMember) \
            .filter(GuildMember.guild_id == guild_id) \
            .all()

    def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildMember]:
        return self.session.query(GuildMember) \
            .filter(GuildMember.guild_id == guild_id) \
            .filter(GuildMember.member_id == member_id) \
            .first()
