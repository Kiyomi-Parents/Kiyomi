from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from src.kiyomi.database import Base


class Guild(Base):
    """Discord guild info and settings"""
    __tablename__ = "guild"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String(128))

    members = relationship("GuildMember", back_populates="guild", cascade="all, delete-orphan")
    channels = relationship("Channel", cascade="all, delete-orphan")
    roles = relationship("Role", cascade="all, delete-orphan")

    def __init__(self, guild_id: int, guild_name: str):
        self.id = guild_id
        self.name = guild_name

    def __str__(self):
        return f"Guild {self.name} ({self.id})"
