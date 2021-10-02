from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from src.database import Base


class Member(Base):
    __tablename__ = "member"

    id = Column(BigInteger, primary_key=True, autoincrement=False)

    name = Column(String(128))

    guilds = relationship("GuildMember", back_populates="member")
    roles = relationship("MemberRole", back_populates="member")

    def __init__(self, member_id: int, name: str):
        self.id = member_id
        self.name = name

    def __str__(self):
        return f"Member {self.name} ({self.id})"
