import pytest


@pytest.fixture
async def role_factory(guild):
    class Factory:
        @staticmethod
        async def make():
            return await guild.create_role(name="Test Role")

    return Factory()


@pytest.fixture
async def role(role_factory):
    return await role_factory.make()
