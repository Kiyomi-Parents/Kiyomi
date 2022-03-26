from abc import ABC, abstractmethod
from typing import List

from src.cogs.general.storage.model.member import Member
from .achievement import Achievement
from ...storage.unit_of_work import UnitOfWork


class AchievementGenerator(ABC):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def get_achievements(self, member: Member) -> List[Achievement]:
        pass

