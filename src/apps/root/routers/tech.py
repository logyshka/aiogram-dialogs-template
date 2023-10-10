from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.common import I18nFunction, OwnerExistsFilter
from src.data.config import Config

router = Router()


@router.message(Command("test"))
async def test_handler(msg: Message, dialog_manager: DialogManager, i18n: I18nFunction):
    await msg.answer(i18n("test"))


@router.message(Command("owner"), OwnerExistsFilter())
async def owner_change(msg: Message, config: Config, i18n: I18nFunction):
    config.main_app.owner_id = msg.from_user.id
    await msg.answer(i18n("owner-changed"))
