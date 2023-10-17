import operator
from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.common import I18nFunction, OwnerExistsFilter
from src.data.config import Config


import operator
from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.common.filters import OwnerExistsFilter
from src.data.config import Config


def register(router: Router, app_name: Optional[str] = None, notification: Optional[str] = None):
    async def change_owner(msg: Message, config: Config, **kwargs):
        nonlocal notification
        if app_name:
            section = operator.attrgetter(app_name)(config)
        else:
            section = config.global_data
        section.owner_id = msg.from_user.id
        i18n = kwargs.get("i18n")
        if i18n:
            notification = i18n(notification)
        await msg.answer(notification)

    router.message.register(change_owner, Command("owner"), OwnerExistsFilter(app_name))
