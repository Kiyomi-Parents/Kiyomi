from __future__ import annotations

import logging
import re
from re import Pattern
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .errors import CogException, ErrorArgResolver, KiyomiException

_logger = logging.getLogger(__name__)


class ErrorResolver:
    _resolvers: List["ErrorArgResolver"] = []
    _arg_pattern: Pattern = re.compile(r"%(\S+)%")

    def add(self, resolver: "ErrorArgResolver"):
        self._resolvers.append(resolver)

    def find_resolver(self, arg_name: str) -> "ErrorArgResolver":
        for resolver in self._resolvers:
            if resolver.arg_name == arg_name:
                return resolver

    async def resolve_arg(self, arg_name: str, arg_value: any, detailed: bool = False) -> str:
        resolver = self.find_resolver(arg_name)

        resolved_arg = str(arg_value)

        if resolver is None:
            _logger.error(
                self.__class__.__name__,
                f"Could not find error arg resolver for arg name {arg_name}",
            )
            return resolved_arg
        
        try:
            if detailed:
                return await resolver.resolve_detailed(arg_value)

            return f"**{await resolver.resolve(arg_value)}**"
        except Exception as error:
            _logger.error(f"{resolver.__class__.__name__}", f"Failed to resolve argument. {error}")
            return resolved_arg
        finally:
            await resolver.service_uow.close()

    async def resolve_message(
        self,
        exception: "CogException",
        message: Optional[str] = None,
        detailed: Optional[bool] = False,
    ) -> str:
        message = message if message is not None else str(exception)
        matches = re.findall(self._arg_pattern, message)

        for arg_name in matches:
            resolved_arg = await self.resolve_arg(arg_name, getattr(exception, arg_name), detailed)
            message = re.sub(self._arg_pattern, resolved_arg, message, 1)

        return message

    @staticmethod
    def resolve_message_simple(
        exception: "KiyomiException",
        message: Optional[str] = None,
        detailed: Optional[bool] = False,
    ) -> str:
        message = message if message is not None else str(exception)
        matches = re.findall(ErrorResolver._arg_pattern, message)

        for arg_name in matches:
            arg_value = getattr(exception, arg_name)

            if not detailed:
                arg_value = f"**{arg_value}**"

            message = re.sub(ErrorResolver._arg_pattern, arg_value, message, 1)

        return message
