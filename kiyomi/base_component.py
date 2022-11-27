from typing import Generic, TypeVar

from kiyomi.kiyomi import Kiyomi
from .base_view import BaseView

T = TypeVar("T", bound=BaseView)


class BaseComponent(Generic[T]):
    def __init__(self, bot: Kiyomi, parent: T):
        self.bot = bot
        self.parent = parent

    async def after_init(self):
        pass
