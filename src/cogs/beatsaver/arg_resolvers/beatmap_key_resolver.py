from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver


class BeatmapKeyResolver(ErrorArgResolver[int, str]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: int) -> str:
        beatmap = self.uow.beatmaps.get_by_id(argument)

        if beatmap is None:
            return f"{argument} (Not in DB)"

        return f"{beatmap}"

    async def resolve(self, argument: int) -> str:
        beatmap = self.uow.beatmaps.get_by_id(argument)

        if beatmap is None:
            return f"{argument}"

        return f"{beatmap.name} ({beatmap.id})"

    @property
    def arg_name(self) -> str:
        return "beatmap_key"
