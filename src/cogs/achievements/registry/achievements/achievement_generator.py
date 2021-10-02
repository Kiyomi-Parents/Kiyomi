from abc import ABC, abstractmethod
from typing import List

from .achievement import Achievement
from ...storage.uow import UnitOfWork
from src.cogs.general.storage.model import Member


class AchievementGenerator(ABC):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def get_achievements(self, member: Member) -> List[Achievement]:
        pass

