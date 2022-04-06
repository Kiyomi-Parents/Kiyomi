from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from src.log import Logger
from .database import Base
from ..utils import Utils

T = TypeVar('T', bound=Base)


class BaseRepository(ABC, Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    def query_by_id(self, entry_id: int) -> Query:
        pass

    def get_by_id(self, entry_id: int) -> Optional[T]:
        return self.query_by_id(entry_id).first()

    @abstractmethod
    def get_all(self) -> Optional[List[T]]:
        pass

    def exists(self, entry_id: int) -> bool:
        return self.get_by_id(entry_id) is not None

    def add(self, entry: T) -> T:
        self.session.add(entry)
        self.commit_changes()
        self.session.refresh(entry)

        Logger.log(entry, "Added")

        return entry

    def add_all(self, entries: List[T]):
        self.session.add_all(entries)
        self.commit_changes()

        for entry in entries:
            self.session.refresh(entry)

        Logger.log(type(entries[0]).__name__, f"Added {len(entries)} new entries")

    def remove(self, entry: T):
        self.session.delete(entry)
        self.commit_changes()

        Logger.log(entry, "Removed")

    def update(self, new_entry: T):
        old_entry = self.get_by_id(new_entry.id)

        Utils.update_class(old_entry, new_entry)

        Logger.log(old_entry, "Updated")

    def commit_changes(self):
        try:
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
