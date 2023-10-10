from typing import Callable, Dict, Any, Awaitable, Union, Optional

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from cachetools import TTLCache

from src.database import User


Event = Union[CallbackQuery, Message]
Handler = Callable[[Event, Dict[str, Any]], Awaitable[Any]]


# Update data with User object from database and prevent spam
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(
            self,
            throttling_rate: float,
            on_process: Optional[Callable[[Handler, Event, Dict[str, Any]], Awaitable[None]]] = None
    ) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=throttling_rate)
        self._on_process = on_process

    async def __call__(
            self,
            handler: Handler,
            event: Event,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id if event.from_user else None

        if user_id:
            if user_id in self.cache:
                return

            data["user"] = await User.get_or_none(id=user_id)

            self.cache[user_id] = None

        if self._on_process:
            await self._on_process(handler, event, data)

        return await handler(event, data)
