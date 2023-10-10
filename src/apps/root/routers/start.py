from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode

from src.data.config import Config
from src.database import User
from ..states import *

router = Router()


@router.message(Command("start"))
async def start(msg: Message, dialog_manager: DialogManager, user: User, config: Config):
    if not user:
        await User.register(
            config=config,
            username=msg.from_user.username,
            user_id=msg.from_user.id
        )
