import discord.ui
from discord import Embed

from src.cogs.beatsaver.storage.model.beatmap import Beatmap
from ..embeds.guild_leaderboard_embed import GuildLeaderboardEmbed
from ..leaderboard_component import LeaderboardComponent
from src.kiyomi import Kiyomi
from src.kiyomi.base_view import BaseView


class GuildLeaderboardButton(LeaderboardComponent, discord.ui.Button):
    def __init__(self, bot: Kiyomi, parent: BaseView, beatmap: Beatmap):
        self.beatmap = beatmap

        LeaderboardComponent.__init__(self, bot, parent)
        discord.ui.Button.__init__(
            self,
            custom_id=f"guild:leaderboard:button:beatmap:{beatmap.id}",
            label="Guild Leaderboard",
            style=discord.enums.ButtonStyle.primary
        )

    async def get_embed(self) -> Embed:
        leaderboard_api = self.bot.get_cog("LeaderboardAPI")

        leaderboard = await leaderboard_api.get_score_leaderboard(self.parent.guild.id, self.parent.beatmap_version_difficulty)

        return GuildLeaderboardEmbed(self.bot, self.parent.message.guild.name, self.parent.beatmap_version_difficulty, leaderboard)

    async def callback(self, interaction: discord.Interaction):
        self.parent.embed = self.get_embed
        await self.parent.update(button_clicked=self)
