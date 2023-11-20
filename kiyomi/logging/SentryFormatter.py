import logging
from logging import Formatter, LogRecord


class SentryFormatter(Formatter):

    dt_fmt = '%Y-%m-%d %H:%M:%S'

    def format(self, record: LogRecord) -> str:
        if record.name.startswith("kiyomi") and len(record.args) > 0:
            record.msg = f"[{record.msg}] " + " ".join(record.args)
            record.args = ()

        formatter = logging.Formatter('{asctime} | {levelname:<8} | {name} | {message}', self.dt_fmt, style='{')

        return formatter.format(record)
