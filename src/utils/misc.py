from typing import *

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import User as AiogramUser
from aiogram_i18n.managers import BaseManager
from src.services.database import User


class I18nManager(BaseManager):
    def __init__(
        self,
        default_locale: Optional[str] = None,
    ):
        super().__init__(default_locale=default_locale)
        self.storage: Dict[StorageKey, str] = {}

    async def get_locale(self, event_from_user: AiogramUser) -> str:
        user = await User.get_or_none(id=event_from_user.id)

        if not user:
            return self.default_locale

        return user.language

    async def set_locale(self, locale: str, state: FSMContext) -> None:
        self.storage[state.key] = locale
