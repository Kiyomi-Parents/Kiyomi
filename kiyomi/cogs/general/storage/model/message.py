from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(BigInteger, primary_key=True, autoincrement=False)

    guild_id = Column(BigInteger, ForeignKey("guild.id"))
    guild = relationship("Guild", back_populates="messages", lazy="raise")

    channel_id = Column(BigInteger, ForeignKey("channel.id"))
    channel = relationship("Channel", back_populates="messages", lazy="raise")

    def __init__(self, guild_id: int, channel_id: int, message_id: int):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.id = message_id

    def __str__(self):
        return f"Message {self.id}"
