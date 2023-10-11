from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

T = TypeVar("T")


class Factory(ABC, Generic[T]):
    @abstractmethod
    def __call__(self, value: str) -> T:
        pass

    @staticmethod
    async def on_error(msg: Message, _widget: TextInput, manager: DialogManager, error: ValueError,):
        error = str(error) or "unknown-error"
        i18n = manager.middleware_data.get("i18n") or (lambda x: x)
        await msg.reply(i18n(error))


