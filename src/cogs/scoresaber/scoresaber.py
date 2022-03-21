from typing import Optional

import discord
from discord import SlashCommandGroup, slash_command
from discord.ext import commands

from src.cogs.general import GeneralAPI
from src.cogs.security import Security
from .errors import PlayerNotFoundException, \
    MemberUsingDifferentPlayerAlreadyException, PlayerRegisteredInGuildAlreadyException, \
    MemberHasPlayerAlreadyRegisteredInGuildException, MemberPlayerNotFoundInGuildException
from .message import Message
from .scoresaber_cog import ScoreSaberCog


class ScoreSaber(ScoreSaberCog, name="Score Saber"):

    @commands.Cog.listener()
    async def on_ready(self):
        await self.player_service.start_scoresaber_api_client()

    player = SlashCommandGroup(
        "player",
        "Link ScoreSaber profile to Discord member."
    )

    @player.command(name="add")
    async def player_add(self, ctx: discord.ApplicationContext, profile: str):
        """Link yourself to your ScoreSaber profile."""
        player_id = self.player_service.scoresaber_id_from_url(profile)
        self.bot.events.emit("register_member", ctx.author)

        try:
            await ctx.respond(f"Getting scores.... This may take a while")
            guild_player = await self.player_service.add_player_with_checks(ctx.interaction.guild_id, ctx.author.id, player_id)
            await ctx.respond(f"Successfully linked **{guild_player.player.name}** ScoreSaber profile!")
        except MemberUsingDifferentPlayerAlreadyException as error:
            await ctx.respond(f"You are linked as **{error.player.name} in another guild!\nYou can't have different Score Saber profiles in different guilds!")
        except PlayerRegisteredInGuildAlreadyException as error:
            await ctx.respond(f"Player **{error.player.player_name}** has already been linked to **{error.member.name}** in this guild!")
        except MemberHasPlayerAlreadyRegisteredInGuildException as error:
            await ctx.respond(f"You have already added yourself as **{error.player.player_name}**!")
        except PlayerNotFoundException as error:
            await ctx.respond(f"Couldn't find player, with ID {error.player_id}, on Score Saber!")

    @player.command(name="remove")
    async def player_remove(self, ctx: discord.ApplicationContext):
        """Remove the currently linked ScoreSaber profile from yourself."""
        try:
            await self.actions.remove_player_with_checks(ctx.guild.id, ctx.author.id)
            await ctx.respond("Successfully unlinked your ScoreSaber account!")
        except MemberPlayerNotFoundInGuildException:
            await ctx.respond("You don't have a ScoreSaber profile linked to yourself.")

    @slash_command(name="showpp")
    async def show_pp(self, ctx: discord.ApplicationContext):
        """Gives bot permission to check the persons PP."""
        guild_player = await self.player_service.get_player_by_guild_id_and_guild_id(ctx.guild.id, ctx.author.id)

        if guild_player is None or guild_player.player.pp == 0:
            await ctx.respond(f"**{ctx.author.name}** doesn't have a PP")
            return

        pp_size = round(guild_player.player.pp / 100)
        await ctx.respond(f"**{ctx.author.name}**'s PP is this big:\n8{'=' * pp_size}D")

    @slash_command(name="recent")
    @Security.owner_or_permissions()
    async def recent_scores(self, ctx: discord.ApplicationContext, discord_member: discord.Member = None, count: int = 1):
        """Displays your most recent scores"""
        if discord_member is None:
            discord_member = ctx.author

        guild_player = await self.player_service.get_player_by_guild_id_and_guild_id(ctx.guild.id, discord_member.id)

        if guild_player is None:
            await ctx.respond("Player not found!")
            return

        if count <= 0:
            await ctx.respond("Score count needs to be positive!")
            return

        try:
            scores = self.score_service.get_recent_scores(guild_player.player.id, count)

            if scores is None:
                await ctx.respond("No scores found!")
                return

            for score in scores:
                score_embed = Message.get_score_embed(guild_player.player, score)
                await ctx.respond(embed=score_embed)

        except IndexError as e:
            await ctx.respond("Song argument too large")

    # TODO: Rename command
    @player.command(name="manualadd", hidden=True)
    @Security.is_owner()
    async def manual_add_player(self, ctx: discord.ApplicationContext, member_id: int, player_id: str, guild_id: Optional[int] = None):
        if guild_id is None:
            guild_id = ctx.interaction.guild_id

        if member_id is None:
            await ctx.respond(f"Please specify a member!")
            return

        general = self.uow.bot.get_cog_api(GeneralAPI)
        member = await general.get_discord_member(guild_id, member_id)
        self.bot.events.emit("register_member", member)

        try:
            guild_player = await self.player_service.add_player(guild_id, member_id, player_id)
            await ctx.respond(f"Successfully linked Score Saber profile {guild_player.player.name} to member {guild_player.member.name} in guild {guild_player.guild.name}")
        except PlayerNotFoundException as error:
            await ctx.respond(f"Could not find Score Saber profile with ID {player_id}")

    # TODO: Rename command
    @player.command(name="manualremove", hidden=True)
    @Security.is_owner()
    async def manual_remove_player(self, ctx: discord.ApplicationContext, member_id: int, player_id: str, guild_id: Optional[int] = None):
        if guild_id is None:
            guild_id = ctx.interaction.guild_id

        if member_id is None:
            await ctx.respond(f"Please specify a member!")
            return

        try:
            guild_player = await self.player_service.remove_player(guild_id, member_id, player_id)
            await ctx.respond(f"Successfully unlinked Score Saber profile {guild_player.player.name} from member {guild_player.member.name} in guild {guild_player.guild.name}!")
        except MemberPlayerNotFoundInGuildException as error:
            await ctx.respond(f"{error.member_id} doesn't have a Score Saber profile with ID {error.player_id} linked in guild {error.guild_id}.")
