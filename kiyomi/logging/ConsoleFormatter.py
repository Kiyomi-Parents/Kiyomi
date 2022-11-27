import copy
import logging
from logging import Formatter, LogRecord

from termcolor import colored


class ConsoleFormatter(Formatter):

    dt_fmt = '%Y-%m-%d %H:%M:%S'

    level_formats = {
        logging.DEBUG: {"color": "blue"},
        logging.INFO: {"color": "green"},
        logging.WARNING: {"color": "yellow"},
        logging.ERROR: {"color": "red"},
        logging.CRITICAL: {"color": 'grey', "attrs": ['bold']}
    }

    def format(self, record: LogRecord) -> str:
        console_record = copy.copy(record)

        level_format = self.level_formats.get(console_record.levelno)

        name_with_color = colored(text=f"{console_record.name}", **level_format)

        if console_record.name.startswith("kiyomi") and len(console_record.args) > 0:
            tag_with_color = colored(text=f"[{console_record.msg}]", **level_format, attrs=["bold"])
            console_record.msg = f"{tag_with_color} " + " ".join(console_record.args)
            console_record.args = ()

        formatter = logging.Formatter('{asctime} | ' + name_with_color + ' | {message}', self.dt_fmt, style='{')
        return formatter.format(console_record)
