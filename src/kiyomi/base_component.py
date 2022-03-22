from pyee import AsyncIOEventEmitter

from src.kiyomi import Kiyomi


class BaseComponent:
    def __init__(self, bot: Kiyomi, events: AsyncIOEventEmitter):
        self.bot = bot
        self.events = events
