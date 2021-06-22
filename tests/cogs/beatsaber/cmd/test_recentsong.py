import pytest
from discord.ext.test import message, verify, empty_queue
from discord.ext.commands.errors import BadArgument

def pytest_generate_tests(metafunc):
    if "player" in metafunc.fixturenames:
        metafunc.parametrize("player", [True, False], indirect=True)

@pytest.fixture()
async def player(request, actions, db_guild, member_factory):
    if request.param:
        await message("!player add 76561198324484050")
        await empty_queue()
    return request.param
   




@pytest.mark.asyncio
async def test_recentsong(player):
    await message("!recentsong")
    if player:
        assert not verify().message().nothing()
        await empty_queue()
    else:
        assert verify() \
            .message() \
            .contains() \
            .content("Player not found!")

@pytest.mark.asyncio
async def test_recentsong_0(player):
    await message("!recentsong 0")
    if player:
        assert not verify().message().nothing()
        await empty_queue()
    else:
        assert verify() \
            .message() \
            .contains() \
            .content("Player not found!")
    
@pytest.mark.asyncio
async def test_recentsong_1(player):
    await message("!recentsong 1")
    if player:
        assert not verify().message().nothing()
        await empty_queue()
    else:
        assert verify() \
            .message() \
            .contains() \
            .content("Player not found!")

@pytest.mark.asyncio
async def test_recentsong_6(player):
    await message("!recentsong 6")
    if player:
        assert not verify().message().nothing()
        await empty_queue()
    else:
        assert verify() \
            .message() \
            .contains() \
            .content("Player not found!")

@pytest.mark.asyncio
async def test_recentsong_negative(player):
    await message("!recentsong -1")
    if player:
        assert not verify().message().nothing()
        await empty_queue()
    else:
        assert verify() \
            .message() \
            .contains() \
            .content("Player not found!")

@pytest.mark.asyncio
async def test_recentsong_string(player):
    with pytest.raises(BadArgument):
        await message("!recentsong afdgqty1346513eqfdvcdfs<fWRYaerhgEG")

        assert verify() \
            .message() \
            .contains() \
            .content("I don't understand what you're trying to do (bad argument)")
    await empty_queue()