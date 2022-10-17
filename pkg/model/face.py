from dataclasses import dataclass
from typing import MutableMapping, Any


@dataclass
class Face:
    fid: int
    long_id: str

    def to_mapping(self) -> MutableMapping[str, Any]:
        return {
            'fid': self.fid,
            'long_id': self.long_id
        }
