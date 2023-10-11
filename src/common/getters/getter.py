from abc import ABC, abstractmethod
from typing import Dict, Any


class Getter(ABC):
    @abstractmethod
    async def __call__(self, *args, **kwargs) -> Dict[str, Any]:
        pass
