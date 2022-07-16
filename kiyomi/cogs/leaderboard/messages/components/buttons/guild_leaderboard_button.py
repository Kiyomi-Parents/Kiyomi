import discord.ui
from discord import Embed

from kiyomi.cogs.beatsaver import BeatSaverAPI
from kiyomi.base_view import BaseView
from ....leaderboard_api import LeaderboardAPI
from ..embeds.guild_leaderboard_embed import GuildLeaderboardEmbed
from ..leaderboard_component import LeaderboardComponent
from kiyomi import Kiyomi


class GuildLeaderboardButton(LeaderboardComponent, discord.ui.Button):
    def __init__(self, bot: Kiyomi, parent: BaseView, song_hash: str):
        self.song_hash = song_hash

        LeaderboardComponent.__init__(self, bot, parent)
        discord.ui.Button.__init__(
            self,
            custom_id=f"guild:leaderboard:button:beatmap:{song_hash}",
            label="Guild Leaderboard",
            style=discord.enums.ButtonStyle.primary,
        )

    async def get_embed(self) -> Embed:
        async with self.bot.get_cog_api(BeatSaverAPI) as beatsaver_api:
            beatmap_difficulty = await beatsaver_api.get_beatmap_difficulty_by_hash(
                self.song_hash,
                self.parent.beatmap_characteristic,
                self.parent.beatmap_difficulty,
            )

        async with self.bot.get_cog_api(LeaderboardAPI) as leaderboard_api:
            leaderboard = await leaderboard_api.get_score_leaderboard(
                self.parent.guild.id,
                self.song_hash,
                self.parent.beatmap_characteristic,
                self.parent.beatmap_difficulty,
            )

        return GuildLeaderboardEmbed(self.bot, self.parent.guild.name, beatmap_difficulty, leaderboard)

    async def callback(self, interaction: discord.Interaction):
        self.parent.embed = self.get_embed
        await self.parent.update(interaction, button_clicked=self)
