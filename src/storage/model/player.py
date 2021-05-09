from sqlalchemy import Column, String, Integer, JSON, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

from src.storage.base import Base
from src.storage.model.discord_guild import guild_player_table

player_role_table = Table('player_role', Base.metadata,
                          Column('player_id', Integer, ForeignKey('player.id')),
                          Column('role_id', Integer, ForeignKey('role.id'))
                          )


class Player(Base):
    """Player data from ScoreSaber"""
    __tablename__ = "player"

    id = Column(Integer, primary_key=True)

    # ScoreSaber info
    playerId = Column(String)
    playerName = Column(String)
    avatar = Column(String)
    rank = Column(Integer)
    countryRank = Column(Integer)
    pp = Column(Float)
    country = Column(String)
    role = Column(String)
    badges = Column(JSON)
    history = Column(String)
    permissions = Column(Integer)
    inactive = Column(Integer)
    banned = Column(Integer)

    guilds = relationship("DiscordGuild", secondary=guild_player_table, back_populates="players")
    scores = relationship("Score")

    # Discord info
    discord_user_id = Column(Integer)
    roles = relationship("DiscordRole", secondary=player_role_table)

    def __init__(self, playerJson):
        self.playerId = playerJson["playerId"]
        self.playerName = playerJson["playerName"]
        self.avatar = playerJson["avatar"]
        self.rank = playerJson["rank"]
        self.countryRank = playerJson["countryRank"]
        self.pp = playerJson["pp"]
        self.country = playerJson["country"]
        self.role = playerJson["role"]
        self.badges = playerJson["badges"]
        self.history = playerJson["history"]
        self.permissions = playerJson["permissions"]
        self.inactive = playerJson["inactive"]
        self.banned = playerJson["banned"]

    @property
    def profile_url(self):
        return f"https://scoresaber.com/u/{self.playerId}"

    @property
    def avatar_url(self):
        return f"https://new.scoresaber.com{self.avatar}"

    @property
    def pp_class(self):
        return self.pp - (self.pp % 1000)

    def __str__(self):
        return f"Player {self.playerName} ({self.playerId})"
