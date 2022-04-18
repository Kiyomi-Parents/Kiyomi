from src.cogs.achievement.services.achievements import Achievement
from src.kiyomi.error import CogException


class AchievementRolesCogException(CogException):
    pass


class UnableToCreateRole(AchievementRolesCogException):
    def __init__(self, guild_id: int, group: str, achievement: Achievement):
        self.guild_id = guild_id
        self.group = group
        self.achievement = achievement

    def __str__(self):
        return f"Unable to create Achievement Role in Guild {self.guild_id} with group {self.group} and identifier " \
               f"{self.achievement.identifier}"
