from typing import List

from src.cogs.general.storage.model.member import Member
from src.cogs.scoresaber import ScoreSaberAPI
from .achievement import Achievement, Condition
from .achievement_generator import AchievementGenerator


class Rank(AchievementGenerator):

    def get_achievements(self, member: Member) -> List[Achievement]:
        achievements = []

        # Generate achievements from 1 to 1k
        for index in range(11):
            achievement_name = self.get_achievement_name(index)
            achievement_condition = self.get_achievement_condition(index, member)
            achievements.append(Achievement(index, achievement_name, achievement_condition))

        return achievements

    @staticmethod
    def get_achievement_name(index: int) -> str:
        if index == 0:
            return f"Rank 1"

        return f"Rank {index * 100}"

    def get_achievement_condition(self, index: int, member: Member) -> Condition:
        def condition() -> bool:
            if member is None:
                return False

            scoresaber = self.bot.get_cog_api(ScoreSaberAPI)
            guild_players = scoresaber.get_guild_players_by_member_id(member.id)

            for guild_player in guild_players:
                if guild_player.player.rank == 0:
                    return False

                player_rank_index = guild_player.player.rank // 100

                if player_rank_index <= index:
                    return True

            return False

        return condition
