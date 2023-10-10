from aiogram.filters import Filter

from src.data.config import Config


class OwnerExistsFilter(Filter):
    async def __call__(self, config: Config):
        return config.main_app.owner_id == 0