from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass
class Schema:
    table_id: str
    column_information: Dict[str, bool]
    nodes: Set[int]
    last_id: int
