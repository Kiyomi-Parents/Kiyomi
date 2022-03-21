from discord import slash_command
from discord.ext import commands

from src.cogs.settings.storage.model.toggle_setting import ToggleSetting
from .services import PlayerLeaderboardService
from .leaderboard_cog import LeaderboardCog
from .message import Message
from src.kiyomi import Kiyomi


class Leaderboard(LeaderboardCog):
    def __init__(self, bot: Kiyomi, player_leaderboard_service: PlayerLeaderboardService):
        super().__init__(bot, player_leaderboard_service)

        # Register events
        self.events()

    def events(self):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            ToggleSetting.create("map_leaderboard", False)
        ]

        self.bot.events.emit("setting_register", settings)

    @slash_command()
    async def song_leaderboard(self, ctx, key: str):
        """Displays song leaderboard."""
        leaderboard = await self.player_leaderboard_service.get_player_score_leaderboard_by_guild_id_and_beatmap_key(ctx.guild.id, key)

        guild_leaderboard_embed = Message.get_player_score_leaderboard_embed(leaderboard)
        await ctx.respond(embed=guild_leaderboard_embed)
