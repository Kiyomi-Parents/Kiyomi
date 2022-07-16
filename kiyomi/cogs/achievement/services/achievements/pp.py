from typing import List

from kiyomi.cogs.general.storage.model.member import Member
from .achievement import Achievement, Condition
from .achievement_generator import AchievementGenerator


class PP(AchievementGenerator):
    def get_achievements(self, member: Member) -> List[Achievement]:
        achievements = []
        total = 21

        # Generate achievements from 0 to 20k
        for index in range(21):
            achievement_name = self.get_achievement_name(index)
            achievement_condition = self.get_achievement_condition(index, member)
            achievements.append(Achievement(total - index, achievement_name, achievement_condition))

        return achievements

    @staticmethod
    def get_achievement_name(index: int) -> str:
        if index == 0:
            return f"<1000 PP"

        return f"{index * 1000} PP"

    def get_achievement_condition(self, index: int, member: Member) -> Condition:
        async def condition() -> bool:
            if member is None:
                return False

            async with self.bot.get_cog("ScoreSaberAPI") as scoresaber:
                guild_players = await scoresaber.get_guild_players_by_member_id(member.id)

            for guild_player in guild_players:
                player_pp_index = guild_player.player.pp // 1000

                if player_pp_index >= index:
                    return True

            return False

        return condition
