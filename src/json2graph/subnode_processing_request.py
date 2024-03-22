from dataclasses import dataclass
from typing import Any


@dataclass
class SubNodeProcessingRequest:
    src_column: str
    level: int
    sub_node: dict[str, Any]
