from .pfp_switcher import PFPSwitcher
from .services.pfp_service import PFPService
from .storage.unit_of_work import UnitOfWork
from .tasks import Tasks
from src.kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    uow = UnitOfWork(await bot.database.get_session())

    pfp_service = PFPService(bot, uow)

    pfp_switcher_tasks = Tasks(bot, pfp_service)

    pfp_switcher_tasks.update_profile_picture.start()

    await bot.add_cog(PFPSwitcher(bot, pfp_service))
