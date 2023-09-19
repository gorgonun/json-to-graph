from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass
class Column:
    name: str
    is_optional: bool
    is_relationship: bool


@dataclass
class Schema:
    id: int
    column_information: Dict[str, Column]
