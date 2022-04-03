from typing import List

from sqlalchemy import types


class StringList(types.TypeDecorator):
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
            if not isinstance(item, str):
                raise RuntimeError(f"Expected object of type str, but got {value.__class__.__name__}")

            items.append(item)

        return ",".join(items)

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        return value.split(",")

    @property
    def python_type(self):
        return List[str]
