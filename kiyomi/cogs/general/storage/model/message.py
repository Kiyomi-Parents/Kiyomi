from datetime import datetime

from sqlalchemy import Column, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(BigInteger, primary_key=True, autoincrement=False)

    guild_id = Column(BigInteger, ForeignKey("guild.id"))
    guild = relationship("Guild", back_populates="messages", lazy="raise")

    channel_id = Column(BigInteger, ForeignKey("channel.id"))
    channel = relationship("Channel", back_populates="messages", lazy="raise")

    created_at = Column(DateTime(timezone=True), nullable=False)

    def __init__(self, guild_id: int, channel_id: int, message_id: int):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.id = message_id
        self.created_at = datetime.utcnow()

    def __str__(self):
        return f"Message {self.id}"
