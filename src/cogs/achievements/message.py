from discord import Embed
from prettytable import PrettyTable

from .registry import AchievementGroups


class Message:
    @staticmethod
    def get_achievements_embed(achievements: AchievementGroups):
        embed = Embed()

        embed.title = "Achievements"

        table = PrettyTable()
        table.border = False
        table.field_names = ["#", "group", "Name", "Complete"]

        index = 0
        for group, achievements in achievements.items():
            for achievement in achievements:
                count = f"{index + 1}"
                group = f"{group}"
                name = achievement.name
                status = f"[{'X' if achievement.complete else ' '}]"
                table.add_row([count, group, name, status])
                index += 1

        embed.description = f"```{table.get_string()}```"

        return embed
