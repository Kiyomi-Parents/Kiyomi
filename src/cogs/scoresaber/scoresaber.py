from typing import Optional

import discord
from discord import SlashCommandGroup, slash_command
from discord.ext import commands

from src.cogs.security import Security
from src.kiyomi.base_cog import BaseCog
from .actions import Actions
from .errors import PlayerExistsException, PlayerNotFoundException, GuildNotFoundException
from .message import Message
from .scoresaber_utils import ScoreSaberUtils
from .storage.uow import UnitOfWork
from .tasks import Tasks


class ScoreSaber(BaseCog, name="Score Saber"):
    def __init__(self, uow: UnitOfWork, tasks: Tasks, actions: Actions):
        self.uow = uow
        self.tasks = tasks
        self.actions = actions

    @commands.Cog.listener()
    async def on_ready(self):
        await self.uow.scoresaber.start()

    player = SlashCommandGroup(
        "player",
        "Link ScoreSaber profile to Discord member."
    )

    @player.command(name="add")
    async def player_add(self, ctx: discord.ApplicationContext, profile: str):
        """Link yourself to your ScoreSaber profile."""
        player_id = ScoreSaberUtils.scoresaber_id_from_url(profile)
        self.uow.bot.events.emit("register_member", ctx.author)

        try:
            await ctx.respond(f"Getting scores.... This may take a while")
            player = await self.actions.add_player(ctx.guild.id, ctx.author.id, player_id)
            await ctx.respond(f"Successfully linked **{player.player_name}** ScoreSaber profile!")
        except (PlayerExistsException, PlayerNotFoundException) as error:
            await ctx.respond(error)

    @player.command(name="remove")
    async def player_remove(self, ctx: discord.ApplicationContext):
        """Remove the currently linked ScoreSaber profile from yourself."""
        try:
            self.actions.remove_player(ctx.guild.id, ctx.author.id)
            await ctx.respond("Successfully unlinked your ScoreSaber account!")
        except (PlayerNotFoundException, GuildNotFoundException) as error:
            await ctx.respond(error)

    @slash_command(name="showpp")
    async def show_pp(self, ctx: discord.ApplicationContext):
        """Gives bot permission to check the persons PP."""
        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_member_id(ctx.guild.id, ctx.author.id)

        if guild_player is None or guild_player.player.pp == 0:
            await ctx.respond(f"**{ctx.author.name}** doesn't have a PP")
            return

        pp_size = round(guild_player.player.pp / 100)
        await ctx.respond(f"**{ctx.author.name}**'s PP is this big:\n8{'=' * pp_size}D")

    @slash_command(name="recent")
    async def recent_score(self, ctx: discord.ApplicationContext, index: int = 0, discord_member: discord.Member = None):
        """Displays your most recent scores"""
        if discord_member is None:
            discord_member = ctx.author

        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_member_id(ctx.guild.id, discord_member.id)

        if guild_player is None:
            await ctx.respond("Player not found!")
            return

        if index < 0:
            await ctx.respond("Score index needs to be positive!")
            return

        try:
            score = self.uow.score_repo.get_player_recent_score(guild_player.player.id, index)

            if score is None:
                await ctx.respond("No scores found!")
                return

            score_embed = Message.get_score_embed(guild_player.player, score)
            await ctx.respond(embed=score_embed)

        except IndexError as e:
            await ctx.respond("Song argument too large")

    @slash_command(name="recentscores")
    @Security.owner_or_permissions()
    async def recent_scores(self, ctx: discord.ApplicationContext, count: int = 1, discord_member: discord.Member = None):
        """Displays your most recent scores"""
        if discord_member is None:
            discord_member = ctx.author

        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_member_id(ctx.guild.id, discord_member.id)

        if guild_player is None:
            await ctx.respond("Player not found!")
            return

        if count <= 0:
            await ctx.respond("Score count needs to be positive!")
            return

        try:
            scores = self.uow.score_repo.get_player_recent_scores(guild_player.player.id, count)

            if scores is None:
                await ctx.respond("No scores found!")
                return

            for score in scores:
                score_embed = Message.get_score_embed(guild_player.player, score)
                await ctx.respond(embed=score_embed)

        except IndexError as e:
            await ctx.respond("Song argument too large")

    # DEBUGGING COMMANDS
    @slash_command(name="getscoresbyid", hidden=True)
    @Security.is_owner()
    async def get_scores_by_id(self, ctx: discord.ApplicationContext, score_id: int):
        db_scores = self.uow.score_repo.get_all_by_score_id(score_id)

        if len(db_scores) == 0:
            await ctx.respond("No scores found!")
            return

        for score in db_scores:
            if score is not None:
                await ctx.respond(f"{score.score} on {score.song_name} at {score.time_set}")
            else:
                await ctx.respond("Score was None")

    @player.command(name="manualadd", hidden=True)
    @Security.is_owner()
    async def manual_add_player(self, ctx: discord.ApplicationContext, player_id: str, member_id: Optional[int], guild_id: Optional[int]):
        if guild_id is None:
            guild_id = ctx.guild.id
        await self.actions.manual_add_player(ctx, player_id, member_id, guild_id)

    @player.command(name="adminadd")
    @Security.owner_or_permissions(administrator=True)
    async def admin_add_player(self, ctx: discord.ApplicationContext, player_id: str, member_id: Optional[int]):
        guild_id = ctx.guild.id
        await self.actions.manual_add_player(ctx, player_id, member_id, guild_id)

    @player.command(name="manualremove", hidden=True)
    @Security.is_owner()
    async def manual_remove_player(self, ctx: discord.ApplicationContext, member_id: Optional[int], guild_id: Optional[int]):
        if guild_id is None:
            guild_id = ctx.guild.id
        await self.actions.manual_remove_player(ctx, member_id, guild_id)

    @player.command(name="adminremove")
    @Security.owner_or_permissions(administrator=True)
    async def admin_remove_player(self, ctx: discord.ApplicationContext, member_id: Optional[int]):
        await self.actions.manual_remove_player(ctx, member_id, ctx.guild.id)
