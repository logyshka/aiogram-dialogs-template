from typing import List, Dict

from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition, OnPageChangedVariants
from aiogram_dialog.widgets.kbd import ScrollingGroup, Keyboard


class ArrowedScrollingGroup(ScrollingGroup):
    def __init__(
            self,
            *buttons: Keyboard,
            id: str = "__arrowedsg__",
            width: int = 1,
            height: int = 5,
            when: WhenCondition = None,
            on_page_changed: OnPageChangedVariants = None,
    ):
        super().__init__(
            *buttons,
            id=id,
            width=width,
            height=height,
            when=when,
            on_page_changed=on_page_changed,
            hide_on_single_page=True
        )

    async def _render_pager(
            self,
            pages: int,
            manager: DialogManager,
    ) -> List[List[InlineKeyboardButton]]:
        if self.hide_pager:
            return []
        if pages == 0 or (pages == 1 and self.hide_on_single_page):
            return []

        last_page = pages - 1
        current_page = min(last_page, await self.get_page(manager))
        next_page = min(last_page, current_page + 1)
        prev_page = max(0, current_page - 1)

        return [
            [
                InlineKeyboardButton(
                    text="◀️",
                    callback_data=self._item_callback_data(prev_page),
                ),
                InlineKeyboardButton(
                    text=f"{current_page + 1}/{pages}",
                    callback_data=self._item_callback_data(current_page),
                ),
                InlineKeyboardButton(
                    text="▶️",
                    callback_data=self._item_callback_data(next_page),
                ),
            ],
        ]

    async def _render_keyboard(
            self,
            data: Dict,
            manager: DialogManager,
    ) -> List[List[InlineKeyboardButton]]:
        keyboard = await self._render_contents(data, manager)
        pages = self._get_page_count(keyboard)

        pager = await self._render_pager(pages, manager)
        page_keyboard = await self._render_page(
            page=await self.get_page(manager),
            keyboard=keyboard,
        )

        return pager + page_keyboard
