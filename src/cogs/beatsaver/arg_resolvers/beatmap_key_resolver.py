from ..services import ServiceUnitOfWork
from src.kiyomi.error import ErrorArgResolver


class BeatmapKeyResolver(ErrorArgResolver[ServiceUnitOfWork, int, str]):
    async def resolve_detailed(self, argument: int) -> str:
        beatmap = self.service_uow.beatmaps.get_by_id(argument)

        if beatmap is None:
            return f"{argument} (Not in DB)"

        return f"{beatmap}"

    async def resolve(self, argument: int) -> str:
        beatmap = self.service_uow.beatmaps.get_by_id(argument)

        if beatmap is None:
            return f"{argument}"

        return f"{beatmap.name} ({beatmap.id})"

    @property
    def arg_name(self) -> str:
        return "beatmap_key"
