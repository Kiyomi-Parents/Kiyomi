from ..services import ServiceUnitOfWork
from src.kiyomi.error import ErrorArgResolver


class RoleIdResolver(ErrorArgResolver[ServiceUnitOfWork, int, str]):
    async def resolve_detailed(self, argument: int) -> str:
        role = await self.service_uow.roles.get_by_id(argument)

        if role is None:
            return f"{argument} (Not in DB)"

        return f"{role}"

    async def resolve(self, argument: int) -> str:
        role = await self.service_uow.roles.get_by_id(argument)

        if role is None:
            return f"{argument}"

        return f"{role.id}"

    @property
    def arg_name(self) -> str:
        return "role_id"
