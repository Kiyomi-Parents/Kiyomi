import copy
import logging
from logging import Formatter, LogRecord


class FileFormatter(Formatter):

    dt_fmt = '%Y-%m-%d %H:%M:%S'

    def format(self, record: LogRecord) -> str:
        file_record = copy.copy(record)

        if file_record.name.startswith("kiyomi") and len(file_record.args) > 0:
            file_record.msg = f"[{file_record.msg}] " + " ".join(file_record.args)
            file_record.args = ()

        formatter = logging.Formatter('{asctime} | {levelname:<8} | {name} | {message}', self.dt_fmt, style='{')

        return formatter.format(file_record)
