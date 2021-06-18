import random

import pytest


@pytest.fixture
def db_role_factory(uow, role_factory):
    class Factory:
        @staticmethod
        async def make(role=None):
            if role is not None:
                return uow.role_repo.add_role(role)

            return uow.role_repo.add_role(await role_factory.make())

    yield Factory()


@pytest.fixture
async def db_role(db_role_factory):
    return await db_role_factory.make()


@pytest.fixture
async def db_role_class_factory(roles):
    class Factory:
        @staticmethod
        async def make(value_class=None):
            if value_class is not None:
                return await roles.create_role(value_class)

            return await roles.create_role(random.randint(1, 100000))

    yield Factory()


@pytest.fixture
async def db_role_class(db_role_class_factory):
    return await db_role_class_factory.make()