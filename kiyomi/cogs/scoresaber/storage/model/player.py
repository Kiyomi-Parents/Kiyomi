import pyscoresaber
from sqlalchemy import Column, String, Integer, Float, BigInteger
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class Player(Base):
    """Player data from ScoreSaber"""

    __tablename__ = "player"

    id = Column(String(128), primary_key=True, autoincrement=False)
    name = Column(String(128))
    avatar = Column(String(128))
    country = Column(String(128))
    pp = Column(Float)
    rank = Column(Integer)
    country_rank = Column(Integer)
    role = Column(String(128))
    history = Column(String(512))
    permissions = Column(Integer)
    banned = Column(Integer)
    inactive = Column(Integer)

    score_stats_total_score = Column(BigInteger)
    score_stats_total_ranked_score = Column(BigInteger)
    score_stats_average_ranked_accuracy = Column(Float)
    score_stats_total_play_count = Column(Integer)
    score_stats_ranked_play_count = Column(Integer)
    score_stats_replays_watched = Column(Integer)

    scores = relationship("Score", back_populates="player", cascade="all, delete-orphan")

    guilds = association_proxy("guild_player", "guild")

    def __init__(self, player_data: pyscoresaber.Player):
        self.id = player_data.id
        self.name = player_data.name
        self.avatar = player_data.profile_picture
        self.country = player_data.country
        self.pp = player_data.pp
        self.rank = player_data.rank
        self.country_rank = player_data.country_rank
        self.role = player_data.role
        self.history = player_data.histories
        self.permissions = player_data.permissions
        self.banned = player_data.banned
        self.inactive = player_data.inactive

        self.score_stats_total_score = player_data.score_stats.total_score
        self.score_stats_total_ranked_score = player_data.score_stats.total_ranked_score
        self.score_stats_average_ranked_accuracy = player_data.score_stats.average_ranked_accuracy
        self.score_stats_total_play_count = player_data.score_stats.total_play_count
        self.score_stats_ranked_play_count = player_data.score_stats.ranked_play_count
        self.score_stats_replays_watched = player_data.score_stats.replays_watched

    @property
    def profile_url(self):
        return f"https://scoresaber.com/u/{self.id}"

    def __str__(self):
        return f"Player {self.name} ({self.id})"
