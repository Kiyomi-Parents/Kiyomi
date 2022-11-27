from typing import List, Type

from kiyomi.cogs.view_persistence.storage.model.persistent_view import PersistentView
from kiyomi import KiyomiException


class MissingPersistentViewClass(KiyomiException):
    def __init__(self, missing_cls_name: str, loaded_cls: List[Type[PersistentView]]):
        self.missing_cls_name = missing_cls_name
        self.loaded_cls = loaded_cls

    def __str__(self):
        return f"Could not locate class {self.missing_cls_name} among {self.loaded_classes}"

    @property
    def loaded_classes(self) -> str:
        return ", ".join([persistent_view.__name__ for persistent_view in self.loaded_cls])
