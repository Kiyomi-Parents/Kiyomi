from __future__ import annotations

import re
from typing import List, Optional, TYPE_CHECKING

from src.log import Logger

if TYPE_CHECKING:
    from src.kiyomi.error import CogException, ErrorArgResolver


class ErrorResolver:
    _resolvers: List["ErrorArgResolver"] = []

    def add(self, resolver: "ErrorArgResolver"):
        self._resolvers.append(resolver)

    def find_resolver(self, arg_name: str) -> "ErrorArgResolver":
        for resolver in self._resolvers:
            if resolver.arg_name == arg_name:
                return resolver

    async def resolve_arg(self, arg_name: str, arg_value: any, detailed: bool = False) -> str:
        resolver = self.find_resolver(arg_name)

        if resolver is None:
            Logger.error(self.__class__.__name__, f"Could not find error arg resolver for arg name {arg_name}")
            return str(arg_value)

        if detailed:
            return await resolver.resolve_detailed(arg_value)

        return f"**{await resolver.resolve(arg_value)}**"

    async def resolve_message(
            self,
            exception: "CogException",
            message: Optional[str] = None,
            detailed: Optional[bool] = False
    ) -> str:
        message = message if message is not None else str(exception)

        pattern = re.compile(r"%(.+)%")
        matches = re.findall(pattern, message)

        for match in matches:
            arg_name = match

            resolved_arg = await self.resolve_arg(arg_name, getattr(exception, arg_name), detailed)

            message = re.sub(pattern, resolved_arg, message)

        return message
