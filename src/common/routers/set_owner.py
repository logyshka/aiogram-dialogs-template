import operator
from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.common import I18nFunction, OwnerExistsFilter
from src.data.config import Config


def register(router: Router, app_name: Optional[str] = None):
    async def change_owner(msg: Message, config: Config, i18n: I18nFunction):
        if app_name:
            section = operator.attrgetter(app_name)(config)
        else:
            section = config.global_data
        section.owner_id = msg.from_user.id
        await msg.answer(i18n("owner-changed"))

    router.message.register(change_owner, Command("owner"), OwnerExistsFilter(app_name))
