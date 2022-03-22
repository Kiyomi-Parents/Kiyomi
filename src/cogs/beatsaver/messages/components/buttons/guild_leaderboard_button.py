import discord.ui
from discord import Embed

from src.cogs.beatsaver.messages.components.beatsaver_component import BeatSaverComponent
from src.cogs.beatsaver.messages.components.embeds.embed import BeatSaverEmbed
from src.cogs.beatsaver.storage import Beatmap
from src.kiyomi import Kiyomi


class GuildLeaderboardButton(BeatSaverComponent, discord.ui.Button):
    def __init__(self, bot: Kiyomi, parent, beatmap: Beatmap):
        BeatSaverComponent.__init__(self, bot, parent, beatmap)
        discord.ui.Button.__init__(
            self,
            custom_id=f"guild:leaderboard:button:beatmap:{beatmap.id}",
            label="Guild Leaderboard",
            style=discord.enums.ButtonStyle.primary
        )

    def get_embed(self) -> Embed:
        embed = BeatSaverEmbed(self.bot)
        embed.title = "temp dummy leaderboard embed"
        embed.description = str(self.parent.beatmap_difficulty)

        return embed

    async def callback(self, interaction: discord.Interaction):
        self.parent.embed = self.get_embed
        await self.parent.update()

        # DO NOT DELETE THIS
        # leaderboard = self.bot.get_cog_api(LeaderboardAPI)
        #
        # guild_leaderboard_embed = await leaderboard.get_player_score_leaderboard_embed(interaction.guild_id, self.beatmap_id)
        #
        # await interaction.response.edit_message(embed=guild_leaderboard_embed)
