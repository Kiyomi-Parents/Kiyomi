import random

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


@pytest.fixture
def db_role_factory(uow, role_factory):
    class factory:
        @staticmethod
        async def make(role=None):
            if role is not None:
                return uow.role_repo.add_role(role)

            return uow.role_repo.add_role(await role_factory.make())

    yield factory()


@pytest.fixture
async def db_role(db_role_factory):
    return await db_role_factory.make()


@pytest.fixture
async def db_role_class_factory(roles):
    class factory:
        @staticmethod
        async def make(value_class=None):
            if value_class is not None:
                return await roles.create_role(value_class)

            return await roles.create_role(random.randint(1, 100000))

    yield factory()


@pytest.fixture
async def db_role_class(db_role_class_factory):
    return await db_role_class_factory.make()
