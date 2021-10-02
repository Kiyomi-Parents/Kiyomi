from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger

from src.database import Base


class Channel(Base):
    __tablename__ = "channel"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    guild_id = Column(BigInteger, ForeignKey("guild.id", ondelete="CASCADE"))

    name = Column(String(128))
