from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass
class Schema:
    table_id: str
    path: list[str]
    column_information: Dict[str, bool]
    last_id: int
