from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver


class RoleIdResolver(ErrorArgResolver[int, str]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: int) -> str:
        role = self.uow.roles.get_by_id(argument)

        if role is None:
            return f"{argument} (Not in DB)"

        return f"{role}"

    async def resolve(self, argument: int) -> str:
        role = self.uow.roles.get_by_id(argument)

        if role is None:
            return f"{argument}"

        return f"{role.id}"

    @property
    def arg_name(self) -> str:
        return "role_id"
