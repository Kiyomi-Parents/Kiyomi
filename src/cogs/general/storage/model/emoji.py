from sqlalchemy import Column, String, ForeignKey, BigInteger

from src.kiyomi.database import Base


class Emoji(Base):
    """Enabled emoji"""
    __tablename__ = "emoji"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    guild_id = Column(BigInteger, ForeignKey("guild.id", ondelete="CASCADE"))
    name = Column(String(128))

    def __init__(self, emoji_id: int, guild_id: int, name: str):
        self.id = emoji_id
        self.guild_id = guild_id
        self.name = name

    def __str__(self):
        return f"Emoji {self.name} ({self.id})"
