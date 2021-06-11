from src.commands.beatsaber.roles import RolesPP, RolesRank, RolesCountryRank
from src.commands.beatsaber.roles.roles import Roles, AlreadyHasRoleException, RoleNotFoundException
from tests.commands.beatsaber import *


def pytest_generate_tests(metafunc):
    if "roles" in metafunc.fixturenames:
        metafunc.parametrize("roles", ["pp", "rank", "countryRank"], indirect=True)


@pytest.fixture
def roles(uow, db_guild, request):
    if request.param == "pp":
        return RolesPP(uow, db_guild)
    elif request.param == "rank":
        return RolesRank(uow, db_guild)
    elif request.param == "countryRank":
        return RolesCountryRank(uow, db_guild)


@pytest.mark.asyncio
async def test_give_player_role_single(roles, db_role, db_player):
    await roles.give_player_role(db_player, db_role)

    assert db_role in db_player.roles
    assert len(db_player.roles) == 1


@pytest.mark.asyncio
async def test_give_player_role_has_role(roles, db_role, uow, db_player):
    await roles.give_player_role(db_player, db_role)

    with pytest.raises(AlreadyHasRoleException):
        await roles.give_player_role(db_player, db_role)

    assert db_role in db_player.roles
    assert len(db_player.roles) == 1


@pytest.mark.asyncio
async def test_give_player_role_no_role_guild(guild, roles, role_factory, db_role_factory, db_player):
    role = await role_factory.make()
    db_role = await db_role_factory.make(role)

    await role.delete()

    assert role not in guild.roles

    with pytest.raises(RoleNotFoundException):
        await roles.give_player_role(db_player, db_role)


@pytest.mark.asyncio
async def test_remove_player_role_single(roles, db_role, db_player):
    await roles.give_player_role(db_player, db_role)
    await roles.remove_player_role(db_player, db_role)

    assert db_role not in db_player.roles
    assert len(db_player.roles) == 0


@pytest.mark.asyncio
async def test_remove_player_roles(roles, db_role_factory, db_player):
    db_role_a = await db_role_factory.make()
    db_role_b = await db_role_factory.make()

    await roles.give_player_role(db_player, db_role_a)
    await roles.give_player_role(db_player, db_role_b)

    await roles.remove_player_roles(db_player, [db_role_a, db_role_b])

    assert db_role_a not in db_player.roles
    assert db_role_b not in db_player.roles
    assert len(db_player.roles) == 0


@pytest.mark.asyncio
async def test_remove_guild_role(roles, db_role, uow, db_guild):
    uow.guild_repo.add_role(db_guild, db_role)

    await roles.remove_guild_role(db_role)

    assert db_role not in db_guild.roles


@pytest.mark.asyncio
async def test_remove_guild_roles(roles, db_role_factory, uow, guild, db_guild_factory):
    db_role_a = await db_role_factory.make()
    db_role_b = await db_role_factory.make()

    db_guild = db_guild_factory.make(guild)

    uow.guild_repo.add_role(db_guild, db_role_a)
    uow.guild_repo.add_role(db_guild, db_role_b)

    await roles.remove_guild_roles([db_role_a, db_role_b])

    assert db_role_a, db_role_b not in db_guild.roles
    assert len(db_guild.roles) == 0

    assert db_role_a, db_role_b not in guild.roles


@pytest.mark.asyncio
async def test_get_role(roles, role, db_role_factory):
    db_role = await db_role_factory.make(role)

    assert role == roles.get_role(db_role)


@pytest.mark.asyncio
async def test_find_guild_role(roles):
    value_class = 1000

    db_role = await roles.create_role(value_class)

    found_db_role = roles.find_guild_role(value_class)

    assert db_role == found_db_role


@pytest.mark.asyncio
async def test_find_player_role(roles, db_player, db_role_class_factory):
    player_skill_class = roles.get_player_skill_class(db_player)

    db_role_class = await db_role_class_factory.make(player_skill_class)

    await roles.give_player_role(db_player, db_role_class)

    db_role = roles.find_player_role(db_player)

    assert db_role_class == db_role


@pytest.mark.asyncio
async def test_create_role(roles, guild):
    db_role = await roles.create_role(1000)

    assert roles.get_role(db_role) in guild.roles


@pytest.mark.asyncio
async def test_update_player_role_empty(roles, db_player):
    await roles.update_player_role(db_player)

    player_skill_class = roles.get_player_skill_class(db_player)

    assert roles.find_guild_role(player_skill_class) is not None
    assert roles.find_player_role(db_player) is not None


@pytest.mark.asyncio
async def test_update_player_role_no_update(roles, db_player):
    await roles.assign_player_role(db_player)

    await roles.update_player_role(db_player)

    player_skill_class = roles.get_player_skill_class(db_player)

    assert roles.find_guild_role(player_skill_class) is not None
    assert roles.find_player_role(db_player) is not None

    assert len(db_player.roles) == 1


@pytest.mark.asyncio
async def test_update_player_role_update(roles, db_player):
    await roles.assign_player_role(db_player)

    db_player.pp = 1000000
    db_player.rank = 0
    db_player.countryRank = 0

    await roles.update_player_role(db_player)

    player_skill_class = roles.get_player_skill_class(db_player)

    assert len(roles.get_guild_roles()) == 2
    assert roles.find_guild_role(player_skill_class) is not None

    assert len(db_player.roles) == 1
    assert roles.find_player_role(db_player) is not None


@pytest.mark.asyncio
async def test_assign_player_role( roles, db_player):
    await roles.assign_player_role(db_player)

    assert roles.find_player_role(db_player) is not None

    player_skill_class = roles.get_player_skill_class(db_player)

    assert roles.find_guild_role(player_skill_class) is not None


@pytest.mark.asyncio
async def test_give_player_role_twice(roles, db_player):
    await roles.assign_player_role(db_player)
    await roles.assign_player_role(db_player)

    assert roles.find_player_role(db_player) is not None

    player_skill_class = roles.get_player_skill_class(db_player)

    assert roles.find_guild_role(player_skill_class) is not None
    assert len(db_player.roles) == 1
    assert len(roles.db_guild.roles) == 1


@pytest.mark.asyncio
async def test_remove_old_player_roles(roles, db_player):
    await roles.assign_player_role(db_player)

    db_player.pp = 1000000
    db_player.rank = 0
    db_player.countryRank = 0

    await roles.remove_old_player_roles(db_player)


@pytest.mark.asyncio
async def test_strip_player_role(roles, db_player):
    await roles.assign_player_role(db_player)

    await roles.strip_player_role(db_player)

    assert roles.find_player_role(db_player) is None


@pytest.mark.asyncio
async def test_strip_guild_roles(roles, db_player_factory):
    db_player_a = db_player_factory.make("76561198029447509")
    db_player_b = db_player_factory.make("76561198324484050")

    await roles.assign_player_role(db_player_a)
    await roles.assign_player_role(db_player_b)

    await roles.strip_guild_roles()

    assert len(db_player_a.roles) == 0
    assert len(db_player_b.roles) == 0
    assert len(roles.db_guild.roles) == 0
