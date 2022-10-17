from dataclasses import dataclass
from typing import MutableMapping, Any, List

from pkg.model.check_time import CheckTime


@dataclass
class User:
    id: int
    name: str
    fid: int
    admin: bool
    check_time: List[CheckTime]

    def to_mapping(self) -> MutableMapping[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'fid': self.fid,
            'admin': self.admin,
            'check_time': [check_time.to_mapping() for check_time in self.check_time]
        }
