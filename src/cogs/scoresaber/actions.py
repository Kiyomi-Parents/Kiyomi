import pyscoresaber

from .storage.uow import UnitOfWork
from .tasks import Tasks
from .errors import PlayerExistsException, PlayerNotFoundException
from .storage.model.guild_player import GuildPlayer
from .storage.model.player import Player


class Actions:
    def __init__(self, uow: UnitOfWork, tasks: Tasks):
        self.uow = uow
        self.tasks = tasks

    def add_player(self, guild_id: int, member_id: int, player_id: str) -> Player:
        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_player_id(guild_id, player_id)

        if guild_player is not None:
            raise PlayerExistsException(f"Player **{guild_player.player.player_name}** has already been added to this guild!")

        guild_player = self.uow.guild_player_repo.get_by_guild_id_and_member_id_and_player_id(guild_id, member_id, player_id)

        if guild_player is not None:
            raise PlayerExistsException(f"You have already added yourself as **{guild_player.player.player_name}**!")

        player = self.get_player(player_id)

        self.uow.guild_player_repo.add(GuildPlayer(guild_id, member_id, player_id))

        # Get player scores
        self.tasks.update_player_scores(player)

        self.uow.bot.events.emit("on_new_player", player)

        # Add role to player
        # await self.update_player_roles(db_community, player) # TODO: Add to event bus

        return player

    def get_player(self, player_id: str) -> Player:
        player = self.uow.player_repo.get_by_id(player_id)

        if player is None:
            try:
                new_player = self.uow.scoresaber.get_player_basic(player_id)

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

