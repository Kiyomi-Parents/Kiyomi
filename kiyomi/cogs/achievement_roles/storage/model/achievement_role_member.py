from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class AchievementRoleMember(Base):
    __tablename__ = "achievement_role_member"

    id = Column(Integer, primary_key=True)

    guild_id = Column(BigInteger, ForeignKey("guild.id"))
    member_id = Column(BigInteger, ForeignKey("member.id"))
    achievement_role_id = Column(Integer, ForeignKey("achievement_role.id"))

    member = relationship("Member", lazy="raise")
    guild = relationship("Guild", lazy="raise")
    achievement_role = relationship("AchievementRole", back_populates="members", lazy="raise")

    def __init__(self, guild_id: int, member_id: int, achievement_role_id: int):
        self.guild_id = guild_id
        self.member_id = member_id
        self.achievement_role_id = achievement_role_id

    def __str__(self):
        return f"Achievement Role Member {self.guild_id} {self.member_id} {self.achievement_role_id}"
