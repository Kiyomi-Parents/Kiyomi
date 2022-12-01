from typing import List, Type, TYPE_CHECKING

from kiyomi import KiyomiException

if TYPE_CHECKING:
    from kiyomi.cogs.view_persistence.storage.model.persistence import Persistence
    from kiyomi.cogs.view_persistence.storage.model.persistent_view import PersistentView


class MissingPersistentViewClass(KiyomiException):
    def __init__(self, missing_cls_name: str, loaded_cls: List[Type["PersistentView"]]):
        self.missing_cls_name = missing_cls_name
        self.loaded_cls = loaded_cls

    def __str__(self):
        return f"Could not locate class {self.missing_cls_name} among {self.loaded_classes}"

    @property
    def loaded_classes(self) -> str:
        return ", ".join([persistent_view.__name__ for persistent_view in self.loaded_cls])


class FailedToLoadPersistentView(KiyomiException):
    def __init__(self, persistence: "Persistence"):
        self.persistence = persistence

    def __str__(self):
        return f"Failed to load persistence class {self.cls_name} with params {self.params}"

    @property
    def cls_name(self) -> str:
        return self.persistence.view_class.__name__

    @property
    def params(self) -> str:
        return ", ".join(self.persistence.get_params())
