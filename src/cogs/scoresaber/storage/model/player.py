import pyscoresaber
from sqlalchemy import Column, String, Integer, JSON, Float
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from src.database import Base


class Player(Base):
    """Player data from ScoreSaber"""
    __tablename__ = "player"

    id = Column(String, primary_key=True)
    player_name = Column(String)
    avatar = Column(String)
    rank = Column(Integer)
    country_rank = Column(Integer)
    pp = Column(Float)
    country = Column(String)
    role = Column(String)
    badges = Column(JSON)
    history = Column(String)
    permissions = Column(Integer)
    inactive = Column(Integer)
    banned = Column(Integer)

    scores = relationship("Score", cascade="all, delete-orphan")

    guilds = association_proxy("guild_player", "guild")

    def __init__(self, player_data: pyscoresaber.Player):
        self.id = player_data.player_id
        self.player_name = player_data.player_name
        self.avatar = player_data.avatar
        self.rank = player_data.rank
        self.country_rank = player_data.country_rank
        self.pp = player_data.pp
        self.country = player_data.country
        self.role = player_data.role
        self.badges = player_data.badges
        self.history = player_data.history
        self.permissions = player_data.permissions
        self.inactive = player_data.inactive
        self.banned = player_data.banned

    @property
    def profile_url(self):
        return f"https://scoresaber.com/u/{self.id}"

    @property
    def avatar_url(self):
        return f"https://new.scoresaber.com{self.avatar}"

    def __str__(self):
        return f"Player {self.player_name} ({self.id})"
