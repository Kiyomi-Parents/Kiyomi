from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

from src.database.database import Database
from src.log import Logger
from src.utils import Utils

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    def __init__(self, database: Database):
        self._db = database

    @abstractmethod
    def get_by_id(self, entry_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> Optional[List[T]]:
        pass

    def add(self, entry: T):
        self._db.add_entry(entry)

        self._db.session.refresh(entry)

    def add_all(self, entries: List[T]):
        self._db.add_entries(entries)

        for entry in entries:
            self._db.session.refresh(entry)

    def remove(self, entry: T):
        self._db.remove_entry(entry)

    def update(self, new_entry: T):
        old_entry = self.get_by_id(new_entry.id)

        Utils.update_class(old_entry, new_entry)

        self._db.commit_changes()
        Logger.log(old_entry, "Updated")
