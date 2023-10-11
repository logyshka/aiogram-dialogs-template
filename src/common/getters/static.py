from typing import Any


class StaticDataGetter:

    def __init__(self, **values: Any) -> None:
        self.values = values

    async def __call__(self, **kwargs) -> dict:
        return self.values
