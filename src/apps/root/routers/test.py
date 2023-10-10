from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.common import I18nFunction


router = Router()


@router.message(Command("test"))
async def test_handler(msg: Message, dialog_manager: DialogManager, i18n: I18nFunction):
    await msg.answer(i18n("test"))
    