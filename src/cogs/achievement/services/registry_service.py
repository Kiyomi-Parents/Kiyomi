from typing import List, Dict

from src.kiyomi import Kiyomi
from src.kiyomi.service.base_basic_service import BaseBasicService
from src.kiyomi.utils import Utils
from .achievements import Achievement, AchievementGenerator
from ..errors import AchievementGeneratorNotFound
from ..storage.storage_unit_of_work import StorageUnitOfWork
from src.cogs.general.storage.model.member import Member

AchievementGroups = Dict[str, List[Achievement]]


class RegistryService(BaseBasicService[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(bot, storage_uow)

        self._generators = []

        for generator in Utils.class_inheritors(AchievementGenerator):
            self._generators.append(generator(bot))

    def _find_generator(self, generator_name: str) -> AchievementGenerator:
        for generator in self._generators:
            if generator.name == generator_name:
                return generator

        raise AchievementGeneratorNotFound(f'Generator with name "{generator_name}" doesn\'t exist.')

    def get_generators(self) -> List[str]:
        return [generator.name for generator in self._generators]

    def get_achievements(self, generator_name: str, member: Member) -> AchievementGroups:
        generator = self._find_generator(generator_name)
        achievement_groups = {generator.name: generator.get_achievements(member)}

        return achievement_groups

    def get_all_achievements(self, member: Member) -> AchievementGroups:
        achievements = {}

        for generator in self._generators:
            achievements[generator.name] = generator.get_achievements(member)

        return achievements

    @staticmethod
    async def _filter_achievements(achievement_groups: AchievementGroups, complete: bool) -> AchievementGroups:
        filtered = {}

        for group, achievements in achievement_groups.items():
            filtered[group] = list()

            for achievement in achievements:
                if await achievement.complete == complete:
                    filtered[group].append(achievement)

        return filtered

    async def get_completed(self, generator_name: str, member: Member) -> AchievementGroups:
        achievement_groups = self.get_achievements(generator_name, member)

        return await self._filter_achievements(achievement_groups, True)

    async def get_uncompleted(self, generator_name: str, member: Member) -> AchievementGroups:
        achievement_groups = self.get_achievements(generator_name, member)

        return await self._filter_achievements(achievement_groups, False)

    async def get_all_completed(self, member: Member) -> AchievementGroups:
        achievement_groups = self.get_all_achievements(member)

        return await self._filter_achievements(achievement_groups, True)

    async def get_all_uncompleted(self, member: Member) -> AchievementGroups:
        achievement_groups = self.get_all_achievements(member)

        return await self._filter_achievements(achievement_groups, False)
