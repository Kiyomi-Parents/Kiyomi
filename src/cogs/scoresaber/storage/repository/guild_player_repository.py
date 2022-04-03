from typing import Optional, List

from sqlalchemy.orm import Query

from src.kiyomi.database import BaseRepository
from ..model.guild_player import GuildPlayer


class GuildPlayerRepository(BaseRepository[GuildPlayer]):

    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(GuildPlayer) \
            .filter(GuildPlayer.id == entry_id)

    def get_all(self) -> Optional[List[GuildPlayer]]:
        return self.session.query(GuildPlayer) \
            .all()

    def get_all_by_guild_id(self, guild_id: int) -> Optional[List[GuildPlayer]]:
        return self.session.query(GuildPlayer) \
            .filter(GuildPlayer.guild_id == guild_id) \
            .all()

    def get_all_by_member_id(self, member_id: int) -> Optional[List[GuildPlayer]]:
        return self.session.query(GuildPlayer) \
            .filter(GuildPlayer.member_id == member_id) \
            .all()

    def get_by_guild_id_and_player_id(self, guild_id: int, player_id: str) -> Optional[GuildPlayer]:
        return self.session.query(GuildPlayer) \
            .filter(GuildPlayer.guild_id == guild_id) \
            .filter(GuildPlayer.player_id == player_id) \
            .first()

    def get_by_guild_id_and_member_id(self, guild_id: int, member_id: int) -> Optional[GuildPlayer]:
        return self.session.query(GuildPlayer) \
            .filter(GuildPlayer.guild_id == guild_id) \
            .filter(GuildPlayer.member_id == member_id) \
            .first()

    def get_by_guild_id_and_member_id_and_player_id(self, guild_id: int, member_id: int, player_id: str) -> Optional[GuildPlayer]:
        return self.session.query(GuildPlayer) \
            .filter(GuildPlayer.guild_id == guild_id) \
            .filter(GuildPlayer.member_id == member_id) \
            .filter(GuildPlayer.player_id == player_id) \
            .first()
