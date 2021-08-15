from discord.ext import commands

from .actions import Actions
from .errors import SongNotFound
from .message import Message
from .storage.uow import UnitOfWork
from src.log import Logger
from src.base.base_cog import BaseCog


class BeatSaver(BaseCog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

        # Register events
        self.events()

    def events(self):

        @self.uow.bot.events.on("on_new_score")
        def attach_song_to_score(score):
            try:
                self.actions.get_beatmap_by_hash(score.song_hash)
            except SongNotFound as error:
                Logger.log(score, error)

    @commands.command(aliases=["bsr", "song"])
    async def map(self, ctx, key: str):
        """Displays song info."""
        leaderboard = self.uow.bot.get_cog("LeaderboardAPI")
        settings = self.uow.bot.get_cog("SettingsAPI")

        try:
            db_beatmap = self.actions.get_beatmap_by_key(key)
            song_embed = Message.get_song_embed(db_beatmap)

            await ctx.send(embed=song_embed)

            if settings.get(ctx.guild.id, "map_leaderboard"):
                leaderboard_embed = leaderboard.get_player_score_leaderboard_embed(ctx.guild.id, key)

                await ctx.send(embed=leaderboard_embed)
        except SongNotFound as error:
            await ctx.send(error)
