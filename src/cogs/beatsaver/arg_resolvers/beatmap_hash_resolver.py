from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver


class BeatmapHashResolver(ErrorArgResolver[int, str]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: int) -> str:
        beatmap_version = self.uow.beatmap_versions.get_by_hash(argument)

        if beatmap_version is None:
            return f"{argument} (Not in DB)"

        return f"{beatmap_version}"

    async def resolve(self, argument: int) -> str:
        beatmap_version = self.uow.beatmap_versions.get_by_hash(argument)

        if beatmap_version is None:
            return f"{argument}"

        return f"{beatmap_version.beatmap.name} ({beatmap_version.map_id})"

    @property
    def arg_name(self) -> str:
        return "beatmap_hash"
