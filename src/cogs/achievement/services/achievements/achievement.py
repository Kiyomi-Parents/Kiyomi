from typing import Callable

Condition = Callable[[], bool]


class Achievement:
    def __init__(self, index: int, name: str, condition: Condition):
        self.index = index
        self.name = name
        self._condition = condition

    @property
    def identifier(self) -> str:
        return f"{self.__class__.__name__}{self.index}"

    @property
    def complete(self) -> bool:
        return self._condition()

    def __str__(self) -> str:
        return f"{self.name} [{'X' if self.complete else ' '}]"
