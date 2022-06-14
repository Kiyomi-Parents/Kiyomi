from .pfp_switcher import PFPSwitcher
from .services.profile_picture_service import ProfilePictureService
from .services.service_unit_of_work import ServiceUnitOfWork
from .storage.storage_unit_of_work import StorageUnitOfWork
from .tasks import Tasks
from src.kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    pfp_switcher_tasks = Tasks(bot, service_uow)

    pfp_switcher_tasks.update_profile_picture.start()

    await bot.add_cog(PFPSwitcher(bot, service_uow))
