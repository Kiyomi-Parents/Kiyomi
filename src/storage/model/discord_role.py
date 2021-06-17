from sqlalchemy import Column, String, Integer, ForeignKey

from src.storage.database import Base


class DiscordRole(Base):
    """Discord role info"""
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey("guild.id", ondelete="CASCADE"))

    # Discord info
    name = Column(String)
    role_id = Column(Integer)

    pp_requirement = Column(Integer)
    rank_requirement = Column(Integer)
    country_rank_requirement = Column(Integer)

    def __init__(self, role):
        self.name = role.name
        self.role_id = role.id

    def __str__(self):
        return f"Discord role {self.name} ({self.role_id})"
