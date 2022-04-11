from .services.spider_graph_service import SpiderGraphService
from src.kiyomi import BaseCog, Kiyomi


class ScoreSaberStatsCog(BaseCog):
    def __init__(self, bot: Kiyomi, spider_graph_service: SpiderGraphService):
        super().__init__(bot)

        self.spider_graph_service = spider_graph_service
