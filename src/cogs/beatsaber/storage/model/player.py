from sqlalchemy import Column, String, Integer, JSON, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

from src.cogs.beatsaber.storage.database import Base
from src.cogs.beatsaber.storage.model.discord_guild import guild_player_table

player_role_table = Table("player_role", Base.metadata,
                          Column("player_id", Integer, ForeignKey("player.id")),
                          Column("role_id", Integer, ForeignKey("role.id"))
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

    scores = relationship("Score", cascade="all, delete-orphan")

    # Discord info
    discord_user_id = Column(Integer)
    guilds = relationship("DiscordGuild", secondary=guild_player_table, back_populates="players")
    roles = relationship("DiscordRole", secondary=player_role_table)

    def __init__(self, player_json):
        self.playerId = player_json["playerId"]
        self.playerName = player_json["playerName"]
        self.avatar = player_json["avatar"]
        self.rank = player_json["rank"]
        self.countryRank = player_json["countryRank"]
        self.pp = player_json["pp"]
        self.country = player_json["country"]
        self.role = player_json["role"]
        self.badges = player_json["badges"]
        self.history = player_json["history"]
        self.permissions = player_json["permissions"]
        self.inactive = player_json["inactive"]
        self.banned = player_json["banned"]
        self.discord_user_id = None

    @property
    def profile_url(self):
        return f"https://scoresaber.com/u/{self.playerId}"

    @property
    def avatar_url(self):
        return f"https://new.scoresaber.com{self.avatar}"

    @property
    def pp_class(self):
        return int(self.pp - (self.pp % 1000))

    @property
    def rank_class(self):
        # This way of getting the rank class is meh, could be better?
        class_num = pow(5, len(str(self.rank))) * 2

        if self.rank % class_num == 0:
            return int(self.rank - (self.rank % class_num))

        return int(self.rank - (self.rank % class_num) + class_num)

    @property
    def country_rank_class(self):
        # TODO: Probably needs to be better....
        class_num = pow(5, len(str(self.rank)))

        if self.rank % class_num == 0:
            return int(self.rank - (self.rank % class_num))

        return int(self.rank - (self.rank % class_num) + class_num)

    def __str__(self):
        return f"Player {self.playerName} ({self.playerId})"
