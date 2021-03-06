from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from src.kiyomi.database import Base


class MemberRole(Base):
    __tablename__ = "member_role"

    id = Column(Integer, primary_key=True)

    guild_id = Column(BigInteger, ForeignKey("guild.id"))
    member_id = Column(BigInteger, ForeignKey("member.id"))
    role_id = Column(BigInteger, ForeignKey("role.id", ondelete="CASCADE"))

    guild = relationship("Guild")
    member = relationship("Member", back_populates="roles")
    role = relationship("Role", back_populates="members")

    def __init__(self, guild_id: int, member_id: int, role_id: int):
        self.guild_id = guild_id
        self.member_id = member_id
        self.role_id = role_id

    def __str__(self):
        return f"Member Role {self.guild_id} {self.member_id} {self.role_id}"
