from datetime import datetime
from typing import Dict


class ActiveZone:
    _datetime_format = "%d/%m_%H:%M"

    def __init__(self, data: Dict):
        self.start = datetime.strptime(data["start"], self._datetime_format)
        self.end = datetime.strptime(data["end"], self._datetime_format)

    @property
    def is_active(self) -> bool:
        now = datetime.utcnow().replace(year=self.start.year)
        return self.start < now < self.end
