from sqlalchemy import Column, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from src.kiyomi.database import Base


class Channel(Base):
    __tablename__ = "channel"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String(128))

    guild_id = Column(BigInteger, ForeignKey("guild.id", ondelete="CASCADE"))
    guild = relationship("Guild", back_populates="channels", uselist=False)

    messages = relationship("Message", back_populates="channel")
