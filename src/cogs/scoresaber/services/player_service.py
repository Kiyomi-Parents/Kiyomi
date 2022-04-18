from typing import List

import pyscoresaber

from src.kiyomi import Kiyomi
from src.log import Logger
from .score_service import ScoreSaberService, ScoreService
from ..errors import MemberUsingDifferentPlayerAlreadyException, PlayerRegisteredInGuildAlreadyException, \
    MemberHasPlayerAlreadyRegisteredInGuildException, PlayerNotFoundException, MemberPlayerNotFoundInGuildException
from ..storage import UnitOfWork
from ..storage.model.guild_player import GuildPlayer
from ..storage.model.player import Player


class PlayerService(ScoreSaberService):
    def __init__(
            self,
            bot: Kiyomi,
            uow: UnitOfWork,
            scoresaber: pyscoresaber.ScoreSaberAPI,
            score_service: ScoreService
    ):
        super().__init__(bot, uow, scoresaber)

        self.score_service = score_service

    async def check_member_player_parity(self, member_id: int, player_id: str):
        """Check if member has another player_id attached to them (Can't register as a different user)"""
        guild_players = self.uow.guild_players.get_all_by_member_id(member_id)

        if guild_players is not None:
            for guild_player in guild_players:
                if guild_player.player_id != player_id:
                    raise MemberUsingDifferentPlayerAlreadyException(member_id, guild_player.player_id)

    async def check_player_registered_guild(self, guild_id: int, player_id: str):
        """Check if the player has already been registered in the guild by someone else"""
        guild_player = self.uow.guild_players.get_by_guild_id_and_player_id(guild_id, player_id)

        if guild_player is not None:
            raise PlayerRegisteredInGuildAlreadyException(guild_id, player_id)

    async def check_member_registered_player_guild(self, guild_id: int, member_id: int, player_id: str):
        """Check if the member has already registered as a player in guild"""
        guild_player = self.uow.guild_players.get_by_guild_id_and_member_id_and_player_id(
                guild_id,
                member_id,
                player_id
        )

        if guild_player is not None:
            raise MemberHasPlayerAlreadyRegisteredInGuildException(guild_id, member_id, player_id)

    async def add_player_with_checks(self, guild_id: int, member_id: int, player_id: str) -> GuildPlayer:
        await self.check_member_player_parity(member_id, player_id)
        await self.check_player_registered_guild(guild_id, player_id)
        await self.check_member_registered_player_guild(guild_id, member_id, player_id)

        return await self.add_player(guild_id, member_id, player_id)

    async def get_player(self, player_id: str) -> Player:
        player = self.uow.players.get_by_id(player_id)

        if player is None:
            try:
                new_player = await self.scoresaber.player_full(int(player_id))

                return self.uow.players.add(Player(new_player))
            except pyscoresaber.NotFoundException as error:
                raise PlayerNotFoundException(player_id) from error

        return player

    async def remove_player_with_checks(self, guild_id: int, member_id: int):
        guild_player = self.uow.guild_players.get_by_guild_id_and_member_id(guild_id, member_id)

        if guild_player is None:
            raise MemberPlayerNotFoundInGuildException(guild_id, member_id)

        return await self.remove_player(guild_id, member_id, guild_player.player_id)

    async def add_player(self, guild_id: int, member_id: int, player_id: str) -> GuildPlayer:
        player = await self.get_player(player_id)

        self.uow.guild_players.add(GuildPlayer(guild_id, member_id, player_id))
        self.uow.save_changes()

        guild_player = self.uow.guild_players.get_by_guild_id_and_member_id_and_player_id(
                guild_id,
                member_id,
                player_id
        )

        self.bot.events.emit("on_new_player", guild_player)

        return guild_player

    async def remove_player(self, guild_id: int, member_id: int, player_id: str) -> GuildPlayer:
        guild_player = self.uow.guild_players.get_by_guild_id_and_member_id_and_player_id(
                guild_id,
                member_id,
                player_id
        )

        if guild_player is None:
            raise MemberPlayerNotFoundInGuildException(guild_id, member_id, player_id)

        self.uow.guild_players.remove(guild_player)
        self.uow.save_changes()

        self.bot.events.emit("on_remove_player", guild_player)

        return guild_player

    async def get_guild_player(self, guild_id: int, member_id: int) -> GuildPlayer:
        guild_player = self.uow.guild_players.get_by_guild_id_and_member_id(guild_id, member_id)

        if guild_player is None:
            raise MemberPlayerNotFoundInGuildException(guild_id, member_id)

        return guild_player

    async def update_player(self, player: Player):
        try:
            new_player = await self.scoresaber.player_full(int(player.id))

            self.uow.players.update(Player(new_player))
            self.uow.save_changes()
        except pyscoresaber.NotFoundException:
            # TODO: rethrow error
            Logger.log(player, "Could not find at ScoreSaber")

    async def get_all_players(self) -> List[Player]:
        return self.uow.players.get_all()

    async def player_exists(self, player_id: str) -> bool:
        return self.uow.players.exists(player_id)
