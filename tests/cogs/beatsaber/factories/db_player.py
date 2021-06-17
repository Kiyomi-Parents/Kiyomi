import pytest


@pytest.fixture
def db_player_factory(uow, member):
    class factory:
        @staticmethod
        def make(scoresaber_id, override_member=None):
            new_player = uow.scoresaber.get_player(scoresaber_id)

            if override_member is not None:
                new_player.discord_user_id = override_member.id
            else:
                new_player.discord_user_id = member.id

            return uow.player_repo.add_player(new_player)

    yield factory()


@pytest.fixture
def db_player(db_player_factory, member):
    return db_player_factory.make("76561198029447509", member)
