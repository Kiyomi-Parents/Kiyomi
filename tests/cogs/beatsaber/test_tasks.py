import itertools

import pytest

from src.utils import Utils


def pytest_generate_tests(metafunc):
    if "players" in metafunc.fixturenames:
        metafunc.parametrize("players", [1, 2, 3], indirect=True)

    available_features = [
        "pp_roles"
    ]

    all_features_combos = []

    for size in range(len(available_features)):
        all_features_combos += list(itertools.combinations(available_features, size))

    print(all_features_combos)

    if "features" in metafunc.fixturenames:
        metafunc.parametrize("features", all_features_combos, indirect=True)

    if "recent_score_channel" in metafunc.fixturenames:
        metafunc.parametrize("recent_score_channel", [False, True], indirect=True)


@pytest.fixture(autouse=True)
async def players(request, actions, db_guild, member_factory):
    scoresaber_ids = [
        "76561198029447509",
        "76561198324484050",
        "76561198881870682"
    ]

    for index in range(request.param):
        member = await member_factory.make()
        await actions.add_player(db_guild.discord_guild_id, member.id, scoresaber_ids[index])


@pytest.fixture(autouse=True)
async def features(request, actions, db_guild):
    for feature in request.param:
        await actions.enable_feature(db_guild.discord_guild_id, feature)


@pytest.fixture(autouse=True)
async def recent_score_channel(request, actions, db_guild, text_channel):
    if request.param:
        actions.add_recent_channel(db_guild.discord_guild_id, text_channel.id)


@pytest.mark.asyncio
async def test_update_players(tasks):
    await tasks.update_players()


@pytest.mark.asyncio
async def test_update_players_guild(tasks, db_guild):
    await tasks.update_players(db_guild)


@pytest.mark.asyncio
async def test_update_player(tasks, db_player):
    tasks.update_player(db_player)


@pytest.mark.asyncio
async def test_update_players_scores(tasks):
    await tasks.update_players_scores()


@pytest.mark.asyncio
async def test_update_players_scores_guild(tasks, db_guild):
    await tasks.update_players_scores(db_guild)


@pytest.mark.asyncio
async def test_update_player_scores(tasks, db_player):
    tasks.update_player_scores(db_player)


# TODO: Implement score factory
@pytest.mark.asyncio
async def test_update_score_song(tasks):
    pass


@pytest.mark.asyncio
async def test_send_notifications(tasks):
    await tasks.send_notifications()


@pytest.mark.asyncio
async def test_send_notifications_guild(tasks, db_guild):
    await tasks.send_notifications(db_guild)


@pytest.mark.asyncio
async def test_send_notification(tasks, db_guild, db_player):
    await tasks.send_notification(db_guild, db_player)


@pytest.mark.asyncio
async def test_update_all_player_roles(tasks):
    await tasks.update_all_player_roles()


@pytest.mark.asyncio
async def test_update_all_player_roles_guild(tasks, db_guild):
    await tasks.update_all_player_roles(db_guild)


@pytest.mark.asyncio
async def test_update_guild_roles(tasks, db_guild):
    await tasks.update_guild_roles(db_guild)
