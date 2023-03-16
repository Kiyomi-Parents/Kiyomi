from typing import List

import pyscoresaber

from kiyomi import Kiyomi, BaseService
from ..errors import (
    MemberUsingDifferentPlayerAlreadyException,
    PlayerRegisteredInGuildAlreadyException,
    MemberHasPlayerAlreadyRegisteredInGuildException,
    PlayerNotFoundException,
    MemberPlayerNotFoundInGuildException,
    PlayerAlreadyExistsException,
)
from ..storage import StorageUnitOfWork
from ..storage.model.guild_player import GuildPlayer
from ..storage.model.player import Player
from ..storage.repository.player_repository import PlayerRepository


class PlayerService(BaseService[Player, PlayerRepository, StorageUnitOfWork]):
    def __init__(
        self,
        bot: Kiyomi,
        repository: PlayerRepository,
        storage_uow: StorageUnitOfWork,
        scoresaber: pyscoresaber.ScoreSaberAPI,
    ):
        super().__init__(bot, repository, storage_uow)

        self.scoresaber = scoresaber

    async def check_member_player_parity(self, member_id: int, player_id: str):
        """Check if member has another player_id attached to them (Can't register as a different user)"""
        guild_players = await self.storage_uow.guild_players.get_all_by_member_id(member_id)

        if guild_players is not None:
            for guild_player in guild_players:
                if guild_player.player_id != player_id:
                    raise MemberUsingDifferentPlayerAlreadyException(member_id, guild_player.player_id)

    async def check_player_registered_guild(self, guild_id: int, player_id: str):
        """Check if the player has already been registered in the guild by someone else"""
        guild_player = await self.storage_uow.guild_players.get_by_guild_id_and_player_id(guild_id, player_id)

        if guild_player is not None:
            raise PlayerRegisteredInGuildAlreadyException(guild_id, player_id)

    async def check_member_registered_player_guild(self, guild_id: int, member_id: int, player_id: str):
        """Check if the member has already registered as a player in guild"""
        guild_player = await self.storage_uow.guild_players.get_by_guild_id_and_member_id_and_player_id(
            guild_id, member_id, player_id
        )

        if guild_player is not None:
            raise MemberHasPlayerAlreadyRegisteredInGuildException(guild_id, member_id, player_id)

    async def add_player_with_checks(self, guild_id: int, member_id: int, player_id: str) -> GuildPlayer:
        await self.check_member_player_parity(member_id, player_id)
        await self.check_player_registered_guild(guild_id, player_id)
        await self.check_member_registered_player_guild(guild_id, member_id, player_id)

        return await self.register_player(guild_id, member_id, player_id)

    async def add_player(self, player_id: str) -> Player:
        player = await self.repository.get_by_id(player_id)

        if player is not None:
            raise PlayerAlreadyExistsException(player_id)

        try:
            new_player = await self.scoresaber.player_full(int(player_id))

            return await self.repository.add(Player(new_player))
        except pyscoresaber.NotFoundException as error:
            raise PlayerNotFoundException(player_id) from error

    async def remove_player_with_checks(self, guild_id: int, member_id: int):
        guild_player = await self.storage_uow.guild_players.get_by_guild_id_and_member_id(guild_id, member_id)

        if guild_player is None:
            raise MemberPlayerNotFoundInGuildException(guild_id, member_id)

        return await self.remove_player(guild_id, member_id, guild_player.player_id)

    async def add_guild_player(self, guild_id: int, member_id: int, player_id: str) -> GuildPlayer:
        return await self.storage_uow.guild_players.add(GuildPlayer(guild_id, member_id, player_id))

    async def register_player(self, guild_id: int, member_id: int, player_id: str) -> GuildPlayer:
        try:
            await self.add_player(player_id)
        except PlayerAlreadyExistsException:
            pass
        guild_player = await self.add_guild_player(guild_id, member_id, player_id)

        self.bot.events.emit("on_new_player", guild_player)

        return guild_player

    async def remove_player(self, guild_id: int, member_id: int, player_id: str) -> GuildPlayer:
        guild_player = await self.storage_uow.guild_players.remove_by_guild_id_and_member_id_and_player_id(
            guild_id, member_id, player_id
        )
        self.bot.events.emit("on_remove_player", guild_player)

        return guild_player

    async def get_guild_player(self, guild_id: int, member_id: int) -> GuildPlayer:
        guild_player = await self.storage_uow.guild_players.get_by_guild_id_and_member_id(guild_id, member_id)

        if guild_player is None:
            raise MemberPlayerNotFoundInGuildException(guild_id, member_id)

        return guild_player

    async def update_player(self, player: str):
        try:
            new_player = await self.scoresaber.player_full(int(player))

            await self.repository.update_entity(Player(new_player))
        except pyscoresaber.NotFoundException as error:
            raise PlayerNotFoundException(player) from error

    async def get_all_player_ids(self) -> List[int]:
        return await self.repository.get_all_player_ids()

    async def get_all_players(self) -> List[Player]:
        return await self.repository.get_all_player()

    async def get_players_with_guild(self) -> List[Player]:
        return await self.repository.get_players_with_guild()

    async def get_all_player_ids_by_guild_id(self, guild_id: int) -> List[int]:
        return await self.repository.get_all_player_ids_by_guild_id(guild_id)