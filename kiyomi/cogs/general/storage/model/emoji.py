from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class Emoji(Base):
    """Enabled emoji"""

    __tablename__ = "emoji"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String(128))

    guild_id = Column(BigInteger, ForeignKey("guild.id", ondelete="CASCADE"))
    guild = relationship("Guild", back_populates="emojis", uselist=False)

    def __init__(self, guild_id: int, emoji_id: int, name: str):
        self.guild_id = guild_id
        self.id = emoji_id
        self.name = name

    def __str__(self):
        return f"Emoji {self.name} ({self.id})"
