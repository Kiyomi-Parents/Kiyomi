from dateutil import parser, tz
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Table
from sqlalchemy.orm import relationship

from src.storage.base import Base

score_guild_table = Table('score_guild', Base.metadata,
                          Column('score_id', Integer, ForeignKey('score.id')),
                          Column('guild_id', Integer, ForeignKey('guild.id'))
                          )


class Score(Base):
    """Score data from ScoreSaber"""
    __tablename__ = "score"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))

    # ScoreSaber info
    rank = Column(Integer)
    scoreId = Column(Integer)
    score = Column(Integer)
    unmodififiedScore = Column(Integer)
    mods = Column(String)
    pp = Column(Float)
    weight = Column(Float)
    timeSet = Column(DateTime)
    leaderboardId = Column(Integer)
    songHash = Column(String)
    songName = Column(String)
    songSubName = Column(String)
    songAuthorName = Column(String)
    levelAuthorName = Column(String)
    difficulty = Column(Integer)
    difficultyRaw = Column(String)
    maxScore = Column(Integer)

    msg_guilds = relationship("DiscordGuild", secondary=score_guild_table)
    song = relationship("Song", uselist=False)

    def __init__(self, scoreJson):
        self.rank = scoreJson["rank"]
        self.scoreId = scoreJson["scoreId"]
        self.score = scoreJson["score"]
        self.unmodififiedScore = scoreJson["unmodififiedScore"]
        self.mods = scoreJson["mods"]
        self.pp = scoreJson["pp"]
        self.weight = scoreJson["weight"]
        self.timeSet = parser.isoparse(scoreJson["timeSet"]).replace(tzinfo=tz.gettz('UTC'))
        self.leaderboardId = scoreJson["leaderboardId"]
        self.songHash = scoreJson["songHash"]
        self.songName = scoreJson["songName"]
        self.songSubName = scoreJson["songSubName"]
        self.songAuthorName = scoreJson["songAuthorName"]
        self.levelAuthorName = scoreJson["levelAuthorName"]
        self.difficulty = scoreJson["difficulty"]
        self.difficultyRaw = scoreJson["difficultyRaw"]
        self.maxScore = scoreJson["maxScore"]

    @property
    def leaderboard_url(self):
        page = (self.rank - 1) // 12 + 1
        return f"http://scoresaber.com/leaderboard/{self.leaderboardId}?page={page}"

    @property
    def song_name_full(self):
        if self.songSubName:
            return f"{self.songName}: {self.songSubName}"
        else:
            return self.songName

    @property
    def difficulty_name(self):
        difficulties = {
            1: "Easy",
            2: "2?",
            3: "Normal",
            4: "4?",
            5: "Hard",
            6: "6?",
            7: "Expert",
            8: "8?",
            9: "Expert Plus"
        }

        return difficulties[self.difficulty]

    @property
    def song_image_url(self):
        return f"https://scoresaber.com/imports/images/songs/{self.songHash}.png"

    @property
    def accuracy(self):
        if self.maxScore:
            return round(self.score / self.maxScore * 100, 3)
        else:
            return "N/A"

    @property
    def weighted_pp(self):
        return round(self.pp * self.weight, 2)

    @property
    def get_date(self):
        return self.timeSet.astimezone(tz.tzlocal())

    def __str__(self):
        return f"Score {self.songName} ({self.scoreId})"
