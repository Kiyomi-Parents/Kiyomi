from sqlalchemy import Column, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class Channel(Base):
    __tablename__ = "channel"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String(128))

    guild_id = Column(BigInteger, ForeignKey("guild.id", ondelete="CASCADE"))
    guild = relationship("Guild", back_populates="channels", uselist=False, lazy="raise")

    messages = relationship("Message", back_populates="channel", lazy="raise")

    def __init__(self, guild_id: int, channel_id: int, channel_name: str):
        self.guild_id = guild_id
        self.id = channel_id
        self.name = channel_name

    def __str__(self):
        return f"Channel {self.name} ({self.id})"
