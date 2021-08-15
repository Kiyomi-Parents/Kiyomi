from discord.ext import commands

from .storage.uow import UnitOfWork
from .tasks import Tasks
from .actions import Actions
from .errors import PlayerExistsException, PlayerNotFoundException, GuildNotFoundException
from .message import Message
from .scoresaber_utils import ScoreSaberUtils
from src.cogs.security import Security
from src.base.base_cog import BaseCog


class ScoreSaber(BaseCog):
    def __init__(self, uow: UnitOfWork, tasks: Tasks, actions: Actions):
        self.uow = uow
        self.tasks = tasks
        self.actions = actions

    @commands.group(invoke_without_command=True)
    async def player(self, ctx):
        """Link ScoreSaber profile to Discord member."""
        await ctx.send_help(ctx.command)

    @player.command(name="add")
    async def player_add(self, ctx, profile: str):
        """Link yourself to your ScoreSaber profile."""
        player_id = ScoreSaberUtils.scoresaber_id_from_url(profile)
        self.uow.bot.events.emit("register_member", ctx.author)

        try:
            player = self.actions.add_player(ctx.guild.id, ctx.author.id, player_id)
            await ctx.send(f"Successfully linked **{player.player_name}** ScoreSaber profile!")
        except (PlayerExistsException, PlayerNotFoundException) as error:
            await ctx.send(error)

    @player.command(name="remove")
    async def player_remove(self, ctx):
        """Remove the currently linked ScoreSaber profile from yourself."""
        try:
            self.actions.remove_player(ctx.guild.id, ctx.author.id)
            await ctx.send("Successfully unlinked your ScoreSaber account!")
        except (PlayerNotFoundException, GuildNotFoundException) as error:
            await ctx.send(error)

    @commands.command(name="showpp")
    async def show_pp(self, ctx):
        """Gives bot permission to check the persons PP."""
        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_member_id(ctx.guild.id, ctx.author.id)

        if guild_player is None or guild_player.player.pp == 0:
            await ctx.send(f"**{ctx.author.name}** doesn't have a PP")
            return

        pp_size = round(guild_player.player.pp / 100)
        await ctx.send(f"**{ctx.author.name}**'s PP is this big:\n8{'=' * pp_size}D")

    @commands.command(aliases=["recentmap", "recentscore"], invoke_without_command=True)
    async def recent_song(self, ctx, index: int = 1, discord_user_id: int = None):
        """Displays your most recent score"""
        if discord_user_id is None:
            discord_user_id = ctx.author.id

        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_member_id(ctx.guild.id, ctx.author.id)

        if guild_player is None:
            await ctx.send("Player not found!")
            return

        if index <= 0:
            index += 1

        try:
            scores = self.uow.score_repo.get_player_recent_scores(guild_player.player.id)

            if scores is None:
                await ctx.send("No scores found!")
                return

            score = scores[index-1]
            score_embed = Message.get_score_embed(guild_player.player, score)
            await ctx.send(embed=score_embed)

        except IndexError as e:
            await ctx.send("Song argument too large")

    # DEBUGGING COMMANDS
    @commands.command(name="getscoresbyid")
    @Security.is_owner()
    async def get_scores_by_id(self, ctx, score_id: int):
        db_scores = self.uow.score_repo.get_all_by_score_id(score_id)

        if len(db_scores) == 0:
            await ctx.send("No scores found!")
            return

        for score in db_scores:
            if score is not None:
                await ctx.send(f"{score.score} on {score.song_name} at {score.time_set}")
            else:
                await ctx.send("Score was None")

    @commands.command(name="manualaddplayer")
    @Security.is_owner()
    async def manual_add_player(self, ctx, discord_member_id: int, scoresaber_player_id: str):
        try:
            player = self.actions.add_player(ctx.guild.id, discord_member_id, scoresaber_player_id)
            await ctx.send(f"Successfully linked **{player.player_name}** ScoreSaber profile to {discord_member_id}!")
        except (PlayerExistsException, PlayerNotFoundException) as error:
            await ctx.send(error)


