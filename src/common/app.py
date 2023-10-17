from typing import Optional, Any, Dict

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from .loader import Loader
from .middlewares import *
from ..data.config import AppConfig


class App:
    def __init__(
            self,
            path: str,
            default_locale: str,
            multi_locale: bool,
            throttling_rate: float = 0.9,
            dispatcher: Optional[Dispatcher] = None
    ):
        self._dispatcher = dispatcher or Dispatcher(storage=MemoryStorage())
        self._loader = Loader(path)
        self.setup_throttling(throttling_rate)
        self.setup_locale(multi_locale, default_locale)
        self._dispatcher.include_routers(
            *self._loader.load_dialogs(),
            *self._loader.load_routers()
        )

    def setup_throttling(self, throttling_rate: float) -> None:
        throttling_middleware = ThrottlingMiddleware(throttling_rate)
        self._dispatcher.message.outer_middleware(throttling_middleware)
        self._dispatcher.callback_query.outer_middleware(throttling_middleware)

    def setup_locale(self, multi_locale: bool, default_locale: str) -> None:
        if multi_locale:
            l10ns = self._loader.load_l10ns(default_locale)
            i18n_middleware = I18NMultiMiddleware(
                l10ns=l10ns,
                default_locale=default_locale
            )
            self._dispatcher.message.middleware(i18n_middleware)
            self._dispatcher.callback_query.middleware(i18n_middleware)

    async def start(
            self,
            config: AppConfig,
            parse_mode: str = ParseMode.HTML,
            context: Optional[Dict[str, Any]] = None,
    ):
        context = context or {}
        bot = Bot(config.bot_token, parse_mode=parse_mode)

        bot_info = await bot.me()
        config.bot_username = bot_info.username

        setup_dialogs(self._dispatcher)
        await self._dispatcher.start_polling(bot, **context)
