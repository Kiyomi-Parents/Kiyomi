from src.cogs.twitch.services.twitch_service import TwitchService


class TwitchUserService(TwitchService):

    async def get_user(self):
        self.twitch.get_users(logins=['your_twitch_username'])