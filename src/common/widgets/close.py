from typing import Any, Optional

from aiogram.types import CallbackQuery
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Text


class Close(Button):
    def __init__(
            self,
            text: Text,
            id: str = "__close__",
            result: Any = None,
            on_click: Optional[OnClick] = None,
            when: WhenCondition = None,
    ):
        super().__init__(
            text=text, on_click=self._on_click,
            id=id, when=when,
        )
        self.text = text
        self.result = result
        self.user_on_click = on_click

    async def _on_click(
            self, callback: CallbackQuery, _button: Button,
            manager: DialogManager,
    ):
        if self.user_on_click:
            await self.user_on_click(callback, self, manager)
        try:
            await callback.message.delete()
        finally:
            await manager.done(self.result)
