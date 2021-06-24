from typing import Union

from dateutil import parser, tz
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Table
from sqlalchemy.orm import relationship

from src.cogs.beatsaber.beatsaber_utils import BeatSaberUtils
from src.cogs.beatsaber.storage.database import Base

score_guild_table = Table("score_guild", Base.metadata,
                          Column("score_id", Integer, ForeignKey("score.id")),
                          Column("guild_id", Integer, ForeignKey("guild.id"))
                          )


class Score(Base):
    """Score data from ScoreSaber"""
    __tablename__ = "score"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("player.id", ondelete="CASCADE"))

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
    song = relationship("Song", uselist=False, cascade="all, delete-orphan")

    def __init__(self, score_json):
        self.rank = score_json["rank"]
        self.scoreId = score_json["scoreId"]
        self.score = score_json["score"]
        self.unmodififiedScore = score_json["unmodififiedScore"]
        self.mods = score_json["mods"]
        self.pp = score_json["pp"]
        self.weight = score_json["weight"]
        self.timeSet = parser.isoparse(score_json["timeSet"]).replace(tzinfo=None)
        self.leaderboardId = score_json["leaderboardId"]
        self.songHash = score_json["songHash"]
        self.songName = score_json["songName"]
        self.songSubName = score_json["songSubName"]
        self.songAuthorName = score_json["songAuthorName"]
        self.levelAuthorName = score_json["levelAuthorName"]
        self.difficulty = score_json["difficulty"]
        self.difficultyRaw = score_json["difficultyRaw"]
        self.maxScore = score_json["maxScore"]

    @property
    def leaderboard_url(self):
        page = (self.rank - 1) // 12 + 1
        return f"https://scoresaber.com/leaderboard/{self.leaderboardId}?page={page}"

    @property
    def song_name_full(self):
        if self.songSubName:
            return f"{self.songName}: {self.songSubName}"

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
            9: "Expert+"
        }

        return difficulties[self.difficulty]

    @property
    def beatsaver_difficulty_name(self):
        difficulties = {
            1: "easy",
            2: "2?",
            3: "normal",
            4: "4?",
            5: "hard",
            6: "6?",
            7: "expert",
            8: "8?",
            9: "expertPlus"
        }

        return difficulties[self.difficulty]

    @property
    def song_image_url(self):
        return f"https://scoresaber.com/imports/images/songs/{self.songHash}.png"

    @property
    def accuracy(self) -> Union[Float, str]:
        max_score = self.maxScore

        if not max_score and self.song is not None:
            song_diff = self.song.difficulties_long[self.beatsaver_difficulty_name]

            if song_diff:
                max_score = BeatSaberUtils.get_max_score(song_diff["notes"])

        if max_score:
            return round(self.score / max_score * 100, 2)

        return "N/A"

    @property
    def weighted_pp(self):
        return round(self.pp * self.weight, 2)

    @property
    def get_date(self):
        return self.timeSet.astimezone(tz.tzlocal())

    def __str__(self):
        return f"Score {self.songName} ({self.scoreId})"
