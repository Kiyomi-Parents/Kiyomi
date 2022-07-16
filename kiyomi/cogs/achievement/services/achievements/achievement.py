from typing import Callable, Awaitable

Condition = Callable[[], Awaitable[bool]]


class Achievement:
    def __init__(self, index: int, name: str, condition: Condition):
        self.index = index
        self.name = name
        self._condition = condition

    @property
    def identifier(self) -> str:
        return f"{self.__class__.__name__}{self.index}"

    @property
    async def complete(self) -> bool:
        return await self._condition()

    def __str__(self) -> str:
        return f"{self.name}"
