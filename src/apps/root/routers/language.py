from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode

from src.common.filters import MultiLocaleFilter
from ..states import *

router = Router()


@router.message(Command("lang"), MultiLocaleFilter())
async def language(_msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=LanguageDialog.root,
        show_mode=ShowMode.EDIT
    )
