from sqlalchemy import Column, String, Integer, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from src.storage.base import Base

guild_player_table = Table('guild_player', Base.metadata,
                           Column('guild_id', Integer, ForeignKey('guild.id')),
                           Column('player_id', Integer, ForeignKey('player.id'))
                           )


class DiscordGuild(Base):
    """Discord guild info and settings"""
    __tablename__ = "guild"

    id = Column(Integer, primary_key=True)

    # Discord info
    discord_guild_id = Column(Integer)
    recent_scores_channel_id = Column(Integer)
    name = Column(String)

    # Features
    pp_roles = Column(Boolean)

    players = relationship("Player", secondary=guild_player_table, back_populates="guilds")
    roles = relationship("DiscordRole", cascade="all, delete-orphan")

    def __init__(self, guild):
        self.discord_guild_id = guild.id
        self.name = guild.name

    def __str__(self):
        return f"Discord guild {self.name} ({self.discord_guild_id})"
