from sqlalchemy import Column, Integer, ForeignKey, String

from src.database import Base


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey("guild.id", ondelete="CASCADE"))

    name = Column(String)
