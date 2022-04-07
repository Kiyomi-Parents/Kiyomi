from prettytable import PrettyTable

from .achievement_embed import AchievementEmbed
from src.kiyomi import Kiyomi
from ...services.registry_service import AchievementGroups


class PlayerAchievementsEmbed(AchievementEmbed):
    def __init__(self, bot: Kiyomi, achievements: AchievementGroups):
        super().__init__(bot)

        self.achievements = achievements

        self.title = "Achievements"

        self.description = f"```{self.get_table}```"

    @property
    def get_table(self) -> str:
        table = PrettyTable()
        table.border = False
        table.field_names = ["#", "group", "Name", "Complete"]

        index = 0
        for group, achievements in self.achievements.items():
            for achievement in achievements:
                count = f"{index + 1}"
                group = f"{group}"
                name = achievement.name
                status = f"[{'X' if achievement.complete else ' '}]"
                table.add_row([count, group, name, status])
                index += 1

        return table.get_string()
