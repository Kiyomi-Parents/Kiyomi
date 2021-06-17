import pytest


@pytest.fixture
async def role_factory(guild):
    class factory:
        @staticmethod
        async def make():
            return await guild.create_role(name="Test Role")

    return factory()


@pytest.fixture
async def role(role_factory):
    return await role_factory.make()
