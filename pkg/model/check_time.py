from dataclasses import dataclass
from typing import MutableMapping, Any


@dataclass
class CheckTime:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    def to_mapping(self) -> MutableMapping[str, Any]:
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'hour': self.hour,
            'minute': self.minute,
            'second': self.second
        }
