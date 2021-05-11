import re


class Utils:
    @staticmethod
    def scoresaber_id_from_url(url):
        pattern = re.compile(r'(https?://scoresaber\.com/u/)?(\d{17})')
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
