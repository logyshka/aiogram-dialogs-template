from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class GetterField:
    name: str
    result_name: Optional[str] = None
    default_value: Optional[Any] = None
