from aiogram.filters import Filter
from aiogram.types import Message

from src.data.config import Config


class OwnerExistsFilter(Filter):
    async def __call__(self, msg: Message, config: Config):
        return config.main_app.owner_id == 0
