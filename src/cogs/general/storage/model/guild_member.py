from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from src.kiyomi.database import Base


class GuildMember(Base):
    __tablename__ = "guild_member"

    id = Column(Integer, primary_key=True)

    guild_id = Column(BigInteger, ForeignKey("guild.id"))
    member_id = Column(BigInteger, ForeignKey("member.id"))

    guild = relationship("Guild", back_populates="members")
    member = relationship("Member", back_populates="guilds")

    def __init__(self, guild_id: int, member_id: int):
        self.guild_id = guild_id
        self.member_id = member_id

    def __str__(self):
        return f"Guild Member {self.guild_id} {self.member_id}"
