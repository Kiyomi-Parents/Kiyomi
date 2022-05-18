from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship, backref

from src.kiyomi.database import Base


class GuildTwitchStreamer(Base):
    __tablename__ = "guild_twitch_streamer"

    id = Column(Integer, primary_key=True)

    guild_id = Column(BigInteger, ForeignKey("guild.id"))
    member_id = Column(BigInteger, ForeignKey("member.id"))
    twitch_streamer_id = Column(String(128), ForeignKey("twitch_streamer.id", ondelete="CASCADE"))

    guild = relationship("Guild")
    member = relationship("Member")
    twitch_streamer = relationship(
            "TwitchStreamer",
            backref=backref("twitch_streamer")
    )

    def __init__(self, guild_id: int, member_id: int, twitch_streamer_id: str):
        self.guild_id = guild_id
        self.member_id = member_id
        self.twitch_streamer_id = twitch_streamer_id

    def __str__(self):
        return f"Twitch Streamer {self.guild_id} {self.member_id} {self.twitch_streamer_id}"
