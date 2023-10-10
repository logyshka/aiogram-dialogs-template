from aiogram.fsm.state import State, StatesGroup


class AdminDialog(StatesGroup):
    root = State()
    channels = State()
    new_channel = State()


class LanguageDialog(StatesGroup):
    root = State()


__all__ = [
    "AdminDialog",
    "LanguageDialog",
]
