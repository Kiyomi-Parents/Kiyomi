from typing import Optional

import pyscoresaber
from discord.ext.commands import Context

from .storage.uow import UnitOfWork
from .tasks import Tasks
from .errors import PlayerExistsException, PlayerNotFoundException, InvalidPlayerException
from .storage.model.guild_player import GuildPlayer
from .storage.model.player import Player


class Actions:
    def __init__(self, uow: UnitOfWork, tasks: Tasks):
        self.uow = uow
        self.tasks = tasks

    async def add_player(self, guild_id: int, member_id: int, player_id: str) -> Player:
        guild_players = self.uow.guild_player_repo.get_all_by_member_id(member_id)

        if guild_players is not None:
            for guild_player in guild_players:
                if guild_player.player_id != player_id:
                    raise InvalidPlayerException(f"You already have a different ScoreSaber user assigned!")

        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_player_id(guild_id, player_id)

        if guild_player is not None:
            raise PlayerExistsException(f"Player **{guild_player.player.player_name}** has already been added to this guild!")

        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_member_id_and_player_id(guild_id, member_id, player_id)

        if guild_player is not None:
            raise PlayerExistsException(f"You have already added yourself as **{guild_player.player.player_name}**!")

        player = await self.get_player(player_id)

        self.uow.guild_player_repo.add(GuildPlayer(guild_id, member_id, player_id))

        # Get player scores
        await self.tasks.update_player_scores(player)

        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_member_id_and_player_id(guild_id, member_id, player_id)

        self.uow.bot.events.emit("on_new_player", guild_player)

        # Add role to player
        # await self.update_player_roles(db_community, player) # TODO: Add to event bus

        return player

    async def get_player(self, player_id: str) -> Player:
        player = self.uow.player_repo.get_by_id(player_id)

        if player is None:
            try:
                new_player = await self.uow.scoresaber.get_player_basic(player_id)

                self.uow.player_repo.add(Player(new_player))
            except pyscoresaber.NotFoundException as error:
                raise PlayerNotFoundException("Could not find player on Score Saber!") from error

        return self.uow.player_repo.get_by_id(player_id)

    def remove_player(self, guild_id: int, member_id: int):
        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_member_id(guild_id, member_id)

        if guild_player is None:
            raise PlayerNotFoundException("You don't have a ScoreSaber profile linked to yourself.")

        self.uow.guild_player_repo.remove(guild_player)

        # Remove player roles
        # await self.remove_player_roles(db_community, db_player) # TODO: Add to event bus

    async def manual_remove_player(self, ctx: Context, member_id: Optional[int], guild_id: Optional[int]):
        if member_id is None:
            member_id = ctx.author.id
        try:
            self.remove_player(guild_id, member_id)
            await ctx.send("Successfully removed!")
        except (PlayerNotFoundException) as error:
            await ctx.send(error)

    async def manual_add_player(self, ctx: Context, player_id: str, member_id: Optional[int], guild_id: Optional[int]):
        if member_id is not None:
            general = self.uow.bot.get_cog("GeneralAPI")
            discord_member = await general.get_discord_member(guild_id, member_id)

            self.uow.bot.events.emit("register_member", discord_member)

        try:
            player = await self.add_player(guild_id, member_id, player_id)
            await ctx.send(f"Successfully linked **{player.player_name}** ScoreSaber profile to {member_id}!")
        except (PlayerExistsException, PlayerNotFoundException, InvalidPlayerException) as error:
            await ctx.send(error)
