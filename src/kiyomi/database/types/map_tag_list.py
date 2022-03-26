from typing import TypeVar, List

import sqlalchemy.types as types
from pybeatsaver import EMapTag

T = TypeVar('T')


class EMapTagList(types.TypeDecorator):
    impl = types.JSON

    def process_literal_param(self, value, dialect):
        pass

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        if not isinstance(value, list):
            raise RuntimeError(f"Expected object of type List, but got {value.__class__.__name__}")

        items = []

        for item in value:
            if not isinstance(item, EMapTag):
                raise RuntimeError(f"Expected object of type EMapTag, but got {value.__class__.__name__}")

            items.append(item.serialize)

        return ",".join(items)

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        items = []
        for item in value.split(","):
            if not EMapTag.has_value(item):
                raise RuntimeError(f"Can't deserialize {item} to EMapTag")

            items.append(EMapTag.deserialize(item))

        return items

    @property
    def python_type(self):
        return List[EMapTag]
