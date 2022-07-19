import json
from pathlib import Path
from types import SimpleNamespace

import logging

from kiyomi import MissingConfigOption, WhitespaceConfigOption, ConfigException

_logger = logging.getLogger(__name__)


class ConfigNamespace(SimpleNamespace):
    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        if len(str(attr).strip()) > 0:
            return attr

        error = WhitespaceConfigOption(item)
        _logger.error("Config", f"{error}")
        raise error

    def __getattr__(self, item):
        error = MissingConfigOption(item)
        _logger.error("Config", f"{error}")
        raise error


class Config:
    __config = None
    CONFIG_PATH = Path(__file__).parent.parent / "config.json"

    @classmethod
    def get(cls) -> ConfigNamespace:
        if cls.__config is None:
            cls.refresh()
        return cls.__config

    @classmethod
    def __read(cls) -> ConfigNamespace:
        with open(cls.CONFIG_PATH, "r") as f:
            return json.load(f, object_hook=lambda d: ConfigNamespace(**d))

    @classmethod
    def refresh(cls):
        cls.__config = cls.__read()
