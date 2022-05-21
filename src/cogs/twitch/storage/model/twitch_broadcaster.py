from sqlalchemy import Column, String
from sqlalchemy.ext.associationproxy import association_proxy
from twitchio import User

from src.kiyomi.database import Base


class TwitchBroadcaster(Base):
    """Broadcaster data from Twitch"""
    __tablename__ = "twitch_broadcaster"

    id = Column(String(128), primary_key=True, autoincrement=False)
    login = Column(String(64))
    display_name = Column(String(64))
    profile_image_url = Column(String(256))
    broadcaster_type = Column(String(32))

    guilds = association_proxy("guild_twitch_broadcaster", "guild")

    def __init__(self, user: User):
        self.id = user.id
        self.login = user.name
        self.display_name = user.display_name
        self.profile_image_url = user.profile_image
        self.broadcaster_type = user.broadcaster_type

    def __str__(self):
        return f"TwitchBroadcaster {self.login} ({self.id})"
