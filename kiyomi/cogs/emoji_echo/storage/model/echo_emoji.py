from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from kiyomi import Base


class EchoEmoji(Base):
    __tablename__ = "echo_emoji"

    id = Column(Integer, primary_key=True, autoincrement=True)

    emoji_id = Column(BigInteger, ForeignKey("emoji.id"))
    emoji = relationship("Emoji", uselist=False, lazy="joined")

    guild_id = Column(BigInteger, ForeignKey("guild.id"))
    guild = relationship("Guild", uselist=False, lazy="joined")

    def __init__(self, emoji_id: int, guild_id: int):
        self.emoji_id = emoji_id
        self.guild_id = guild_id

    def __str__(self):
        return f"Echo Emoji {self.emoji_id} ({self.id})"
