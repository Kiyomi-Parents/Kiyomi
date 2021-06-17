import pytest

from src.cogs.beatsaber import BeatSaberUtils, FeatureFlagException
from src.cogs.beatsaber.actions import GuildNotFoundException, GuildRecentChannelExistsException, GuildRecentChannelNotFoundException


def pytest_generate_tests(metafunc):
    if "feature_flag" in metafunc.fixturenames:
        metafunc.parametrize("feature_flag", ["pp_roles"], indirect=True)


@pytest.fixture
def feature_flag(request):
    return request.param


@pytest.fixture
def feature(feature_flag, uow, db_guild):
    feature_class = BeatSaberUtils.get_feature(feature_flag)
    return feature_class(uow, db_guild)


@pytest.fixture
async def enable_feature(feature):
    await feature.set(True)


@pytest.fixture
async def disable_feature(feature):
    await feature.set(False)


@pytest.mark.asyncio
async def test_add_player(actions, db_guild, member):
    db_player = await actions.add_player(db_guild.discord_guild_id, member.id, "76561198029447509")

    assert db_player is not None
    assert db_player.discord_user_id == member.id
    assert len(db_player.scores) != 0
    assert len(db_player.guilds) != 0
    assert db_player.guilds[0] == db_guild


@pytest.mark.asyncio
async def test_add_player_feature(actions, db_guild, member, enable_feature):
    db_player = await actions.add_player(db_guild.discord_guild_id, member.id, "76561198029447509")

    assert db_player is not None
    assert db_player.discord_user_id == member.id
    assert len(db_player.scores) != 0
    assert len(db_player.guilds) != 0
    assert db_player.guilds[0].discord_guild_id == db_guild.discord_guild_id
    assert len(db_player.roles) == 1
    assert len(member.roles) == 2


@pytest.mark.asyncio
async def test_add_player_no_guild(actions, guild, member):
    with pytest.raises(GuildNotFoundException):
        await actions.add_player(guild.id, member.id, "76561198029447509")


@pytest.mark.asyncio
async def test_remove_player(actions, uow, db_guild, member):
    pre_db_player = await actions.add_player(db_guild.discord_guild_id, member.id, "76561198029447509")

    post_db_player = await actions.remove_player(db_guild.discord_guild_id, member.id)

    assert pre_db_player == post_db_player
    assert uow.player_repo.get_player_by_member_id(member.id) is None
    assert len(uow.player_repo.get_players()) == 0
    assert len(uow.score_repo.get_scores()) == 0
    assert len(uow.song_repo.get_songs()) == 0


@pytest.mark.asyncio
async def test_update_player_roles(actions, db_guild, db_player_factory, member, enable_feature):
    db_player = db_player_factory.make("76561198029447509", member)

    await actions.update_player_roles(db_guild, db_player)

    assert len(member.roles) == 2


@pytest.mark.asyncio
async def test_remove_player_roles(actions, db_guild, db_player_factory, member, enable_feature):
    db_player = db_player_factory.make("76561198029447509", member)
    await actions.update_player_roles(db_guild, db_player)

    assert len(member.roles) == 2

    await actions.remove_player_roles(db_guild, db_player)

    assert len(member.roles) == 1


@pytest.mark.asyncio
async def test_add_recent_channel(actions, db_guild, text_channel):
    actions.add_recent_channel(db_guild.discord_guild_id, text_channel.id)

    assert db_guild.recent_scores_channel_id == text_channel.id


@pytest.mark.asyncio
async def test_add_recent_channel_already_assigned(actions, db_guild, text_channel_factory):
    text_channel_a = await text_channel_factory.make()
    text_channel_b = await text_channel_factory.make()

    actions.add_recent_channel(db_guild.discord_guild_id, text_channel_a.id)

    with pytest.raises(GuildRecentChannelExistsException):
        actions.add_recent_channel(db_guild.discord_guild_id, text_channel_b.id)


@pytest.mark.asyncio
async def test_remove_recent_channel_empty(actions, db_guild):
    with pytest.raises(GuildRecentChannelNotFoundException):
        actions.remove_recent_channel(db_guild.discord_guild_id)


@pytest.mark.asyncio
async def test_remove_recent_channel(actions, db_guild, text_channel):
    actions.add_recent_channel(db_guild.discord_guild_id, text_channel.id)

    actions.remove_recent_channel(db_guild.discord_guild_id)

    assert db_guild.recent_scores_channel_id is None


@pytest.mark.asyncio
async def test_enable_feature(actions, db_guild, feature_flag):
    await actions.enable_feature(db_guild.discord_guild_id, feature_flag)

    with pytest.raises(FeatureFlagException):
        await actions.enable_feature(db_guild.discord_guild_id, feature_flag)

    assert hasattr(db_guild, feature_flag)
    assert getattr(db_guild, feature_flag)


@pytest.mark.asyncio
async def test_disable_feature(actions, db_guild, feature_flag):
    with pytest.raises(FeatureFlagException):
        await actions.disable_feature(db_guild.discord_guild_id, feature_flag)

    await actions.enable_feature(db_guild.discord_guild_id, feature_flag)

    await actions.disable_feature(db_guild.discord_guild_id, feature_flag)

    assert hasattr(db_guild, feature_flag)
    assert not getattr(db_guild, feature_flag)
