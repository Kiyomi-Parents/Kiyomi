from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Role(Base):
    """Discord role info"""
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey("guild.id", ondelete="CASCADE"))

    name = Column(String)

    members = relationship("MemberRole", back_populates="role")

    def __init__(self, role_id: int, guild_id: int, name: str):
        self.id = role_id
        self.guild_id = guild_id
        self.name = name

    def __str__(self):
        return f"Role {self.name} ({self.id})"
