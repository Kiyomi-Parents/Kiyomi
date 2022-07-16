from ..storage import StorageUnitOfWork
from ..storage.model.guild_player import GuildPlayer
from ..storage.repository.guild_player_repository import GuildPlayerRepository
from kiyomi import BaseService


class GuildPlayerService(BaseService[GuildPlayer, GuildPlayerRepository, StorageUnitOfWork]):
    pass
