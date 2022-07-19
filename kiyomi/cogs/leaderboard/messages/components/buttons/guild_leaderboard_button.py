import discord.ui
from discord import Embed

from kiyomi.base_view import BaseView
from kiyomi.cogs.scoresaber import ScoreSaberAPI
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

    async def after_init(self):
        async with self.bot.get_cog("SettingsAPI") as settings:
            emoji = await settings.get_override_or_default(self.parent.guild.id, "guild_leaderboard_emoji")

        if emoji:
            self.label = None
            self.emoji = emoji

        async with self.bot.get_cog_api(ScoreSaberAPI) as scoresaber_api:
            leaderboard = await scoresaber_api.get_leaderboard(self.song_hash, self.parent.beatmap_characteristic, self.parent.beatmap_difficulty)

        if leaderboard is None:
            self.parent.remove_item(self)

    async def get_embed(self) -> Embed:
        async with self.bot.get_cog_api(LeaderboardAPI) as leaderboard_api:
            guild_leaderboard = await leaderboard_api.get_guild_leaderboard(
                self.parent.guild.id,
                self.song_hash,
                self.parent.beatmap_characteristic,
                self.parent.beatmap_difficulty,
            )

        return GuildLeaderboardEmbed(self.bot, self.parent.guild.name, guild_leaderboard)

    async def callback(self, interaction: discord.Interaction):
        self.parent.embed = self.get_embed
        await self.parent.update(interaction, button_clicked=self)
