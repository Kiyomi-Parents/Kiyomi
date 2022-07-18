from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class SentScore(Base):
    __tablename__ = "sent_score"

    id = Column(Integer, primary_key=True)

    score_id = Column(Integer, ForeignKey("score.id"))
    guild_id = Column(BigInteger, ForeignKey("guild.id"))

    score = relationship("Score", lazy="joined")
    guild = relationship("Guild", lazy="joined")

    def __init__(self, score_id: int, guild_id: int):
        self.score_id = score_id
        self.guild_id = guild_id

    def __str__(self):
        return f"Sent Score {self.score_id} in {self.guild_id}"
