from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from kiyomi.database import Base


class GuildTwitchBroadcaster(Base):
    __tablename__ = "guild_twitch_broadcaster"

    id = Column(Integer, primary_key=True)

    guild_id = Column(BigInteger, ForeignKey("guild.id"))
    member_id = Column(BigInteger, ForeignKey("member.id"))
    twitch_broadcaster_id = Column(String(128), ForeignKey("twitch_broadcaster.id", ondelete="CASCADE"))

    guild = relationship("Guild", lazy="joined")
    member = relationship("Member", lazy="joined")
    twitch_broadcaster = relationship("TwitchBroadcaster", back_populates="guild_twitch_broadcasters", lazy="joined")

    def __init__(self, guild_id: int, member_id: int, twitch_broadcaster_id: str):
        self.guild_id = guild_id
        self.member_id = member_id
        self.twitch_broadcaster_id = twitch_broadcaster_id

    def __str__(self):
        return f"GuildTwitchBroadcaster {self.guild_id} {self.member_id} {self.twitch_broadcaster_id}"
