import discord.ui
from discord import Embed

from src.cogs.leaderboard import LeaderboardAPI
from src.kiyomi import Kiyomi


class GuildLeaderboardButton(discord.ui.Button):
    def __init__(self, bot: Kiyomi, beatmap_id: str):
        super().__init__(
            label="Guild Leaderboard",
            style=discord.enums.ButtonStyle.primary,
            custom_id=str(beatmap_id),
        )

        self.bot = bot
        self.beatmap_id = beatmap_id

    async def callback(self, interaction: discord.Interaction):
        leaderboard = self.bot.get_cog_api(LeaderboardAPI)

        guild_leaderboard_embed = await leaderboard.get_player_score_leaderboard_embed(interaction.guild_id, self.beatmap_id)

        await interaction.response.edit_message(embed=guild_leaderboard_embed)
