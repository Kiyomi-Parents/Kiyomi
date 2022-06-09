from sqlalchemy.ext.asyncio import AsyncSession

from .repository.profile_picture_repository import ProfilePictureRepository
from src.kiyomi import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.profile_pictures = ProfilePictureRepository()
