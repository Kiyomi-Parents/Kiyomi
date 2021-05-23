import re
import time

from src.log import Logger
from functools import wraps


class Utils:
    @staticmethod
    def scoresaber_id_from_url(url):
        pattern = re.compile(r'(https?://scoresaber\.com/u/)?(\d{16,17})')
        match = re.match(pattern, url)

        if match:
            return match.group(2)

        return None

    @staticmethod
    def is_player_in_guild(db_player, guild_id):
        for db_guild in db_player.guilds:
            if db_guild.discord_guild_id == guild_id:
                return True

        return False

    @staticmethod
    def time_task(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            Logger.log(func.__name__, "<===> Starting task <===>")
            start_time = time.process_time()
            res = await func(self, *args, **kwargs)
            Logger.log(func.__name__, f"Finished task in {round(time.process_time() - start_time, 2)} seconds\n")

            return res

        return wrapper

    @staticmethod
    def discord_ready(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not self.uow.client.is_ready():
                Logger.log("Discord", "Discord client not ready, skipping task update players")
                return

            return await func(self, *args, **kwargs)

        return wrapper
