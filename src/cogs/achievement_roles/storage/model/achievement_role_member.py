from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class AchievementRoleMember(Base):
    __tablename__ = "achievement_role_member"

    id = Column(Integer, primary_key=True)

    guild_id = Column(Integer, ForeignKey("guild.id"))
    member_id = Column(Integer, ForeignKey("member.id"))
    achievement_role_id = Column(Integer, ForeignKey("achievement_role.id"))

    member = relationship("Member")
    guild = relationship("Guild")
    achievement_role = relationship("AchievementRole", back_populates="members")

    def __init__(self, guild_id: int, member_id: int, achievement_role_id: int):
        self.guild_id = guild_id
        self.member_id = member_id
        self.achievement_role_id = achievement_role_id

    def __str__(self):
        return f"Achievement Role Member {self.guild_id} {self.member_id} {self.achievement_role_id}"
