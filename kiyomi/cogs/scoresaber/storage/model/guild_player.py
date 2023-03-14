from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class GuildPlayer(Base):
    __tablename__ = "guild_player"

    id = Column(Integer, primary_key=True)

    guild_id = Column(BigInteger, ForeignKey("guild.id"))
    member_id = Column(BigInteger, ForeignKey("member.id"))
    player_id = Column(String(128), ForeignKey("player.id", ondelete="CASCADE"))

    guild = relationship("Guild", lazy="selectin")
    member = relationship("Member", lazy="selectin")
    player = relationship("Player", back_populates="guild_players", lazy="selectin")

    def __init__(self, guild_id: int, member_id: int, player_id: str):
        self.guild_id = guild_id
        self.member_id = member_id
        self.player_id = player_id

    def __str__(self):
        return f"Guild Player {self.guild_id} {self.member_id} {self.player_id}"
