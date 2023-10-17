from typing import Dict, Callable, Any, Awaitable, Union

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization

Data = Dict[str, Any]
I18nFunction = Union[
    Callable[[str, Data], str],
    Callable[[str], str]
]
Event = Union[
    CallbackQuery,
    Message
]
Handler = Callable[[Event, Data], Awaitable[Any]]


class I18NMultiMiddleware(BaseMiddleware):
    def __init__(self, l10ns: Dict[str, FluentLocalization], default_locale: str):
        self.l10ns = l10ns
        self.default_locale = default_locale

    async def __call__(
            self,
            handler: Handler,
            event: Event,
            data: Data,
    ) -> Any:
        user = data.get("user")

        if user:
            language = user.language
        else:
            language = self.default_locale

        data["current_language"] = language
        data["i18n"] = self.l10ns[language].format_value
        data["l10ns"] = self.l10ns
        return await handler(event, data)
