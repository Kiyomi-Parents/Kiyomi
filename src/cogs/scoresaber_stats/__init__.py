from .scoresaber_stats import ScoreSaberStats
from .services.spider_graph_service import SpiderGraphService
from .storage.unit_of_work import UnitOfWork
from ...kiyomi import Kiyomi


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    spider_graph_service = SpiderGraphService(bot, uow)

    bot.add_cog(ScoreSaberStats(bot, spider_graph_service))
