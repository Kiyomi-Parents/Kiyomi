from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, backref

from src.database import Base


class GuildPlayer(Base):
    __tablename__ = "guild_player"

    id = Column(Integer, primary_key=True)

    guild_id = Column(Integer, ForeignKey("guild.id"))
    member_id = Column(Integer, ForeignKey("member.id"))
    player_id = Column(String, ForeignKey("player.id"))

    guild = relationship("Guild")
    member = relationship("Member")
    player = relationship("Player", backref=backref("guild_player"))

    def __init__(self, guild_id: int, member_id: int, player_id: str):
        self.guild_id = guild_id
        self.member_id = member_id
        self.player_id = player_id

    def __str__(self):
        return f"Guild Player {self.guild_id} {self.member_id} {self.player_id}"
