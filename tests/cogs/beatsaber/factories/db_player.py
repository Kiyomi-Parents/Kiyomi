import pytest

from src.cogs.beatsaber.storage.model.player import Player


@pytest.fixture
def db_player_factory(uow, member):
    class Factory:
        @staticmethod
        def make(scoresaber_id, override_member=None):
            new_player = uow.scoresaber.get_player_basic(scoresaber_id)
            player = Player(new_player)

            if override_member is not None:
                player.discord_user_id = override_member.id
            else:
                player.discord_user_id = member.id

            return uow.player_repo.add_player(player)

    yield Factory()


@pytest.fixture
def db_player(db_player_factory, member):
    return db_player_factory.make("76561198029447509", member)
