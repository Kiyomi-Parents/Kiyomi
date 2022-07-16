from ..services import ServiceUnitOfWork
from kiyomi.error import ErrorArgResolver


class BeatmapHashResolver(ErrorArgResolver[ServiceUnitOfWork, int, str]):
    async def resolve_detailed(self, argument: int) -> str:
        beatmap_version = await self.service_uow.beatmap_versions.get_by_hash(argument)

        if beatmap_version is None:
            return f"{argument} (Not in DB)"

        return f"{beatmap_version}"

    async def resolve(self, argument: int) -> str:
        beatmap_version = await self.service_uow.beatmap_versions.get_by_hash(argument)

        if beatmap_version is None:
            return f"{argument}"

        return f"{beatmap_version.beatmap.name} ({beatmap_version.map_id})"

    @property
    def arg_name(self) -> str:
        return "beatmap_hash"
