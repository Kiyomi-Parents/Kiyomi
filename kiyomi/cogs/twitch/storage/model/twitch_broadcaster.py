from sqlalchemy import Column, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from twitchio import User

from kiyomi.database import Base


class TwitchBroadcaster(Base):
    """Broadcaster data from Twitch"""

    __tablename__ = "twitch_broadcaster"

    id = Column(String(128), primary_key=True, autoincrement=False)
    login = Column(String(64))
    display_name = Column(String(64))
    profile_image_url = Column(String(256))
    broadcaster_type = Column(String(32))

    guild_twitch_broadcasters = relationship("GuildTwitchBroadcaster", back_populates="twitch_broadcaster", lazy="joined")
    guilds = association_proxy("guild_twitch_broadcasters", "guild")

    def __init__(self, user: User):
        self.id = user.id
        self.login = user.name
        self.display_name = user.display_name
        self.profile_image_url = user.profile_image
        self.broadcaster_type = user.broadcaster_type

    def __str__(self):
        return f"TwitchBroadcaster {self.login} ({self.id})"
