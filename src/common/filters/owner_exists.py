import operator
from typing import Optional

from aiogram.filters import Filter
from aiogram.types import Message

from src.data.config import Config, IOwnable


class OwnerExistsFilter(Filter):
    def __init__(self, app_name: Optional[str] = None):
        self.app_name = app_name

    async def __call__(self, msg: Message, config: Config):
        section: IOwnable
        if self.app_name:
            section = operator.attrgetter(self.app_name)(config)
        else:
            section = config.global_data
        return section.owner_id == 0
