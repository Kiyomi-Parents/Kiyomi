from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class AchievementRole(Base):
    """Discord role info"""

    __tablename__ = "achievement_role"

    id = Column(Integer, primary_key=True)

    group = Column(String(128))
    identifier = Column(String(128))

    members = relationship(
        "AchievementRoleMember",
        back_populates="achievement_role",
        cascade="all, delete",
    )

    guild_id = Column(BigInteger, ForeignKey("guild.id", ondelete="CASCADE"))
    guild = relationship("Guild")

    role_id = Column(BigInteger, ForeignKey("role.id", ondelete="CASCADE"))
    role = relationship("Role", cascade="all, delete")

    def __init__(self, guild_id: int, role_id: int, group: str, identifier: str):
        self.guild_id = guild_id
        self.role_id = role_id
        self.group = group
        self.identifier = identifier

    def __str__(self):
        return f"Achievement role {self.group}/{self.identifier} ({self.id})"
