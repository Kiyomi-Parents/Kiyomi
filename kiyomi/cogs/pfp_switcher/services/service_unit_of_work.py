from .profile_picture_service import ProfilePictureService
from ..storage import StorageUnitOfWork
from kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(storage_uow)

        self.profile_pictures = ProfilePictureService(bot, storage_uow.profile_pictures, storage_uow)
