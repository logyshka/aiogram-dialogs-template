import operator

from aiogram_dialog.widgets.common.items import ItemsGetterVariant
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.kbd.list_group import ItemIdGetter
from aiogram_dialog.widgets.text import Text


class ItemsSelect(Select):
    def __init__(
            self,
            text: Text,
            id: str = "items",
            item_id_getter: ItemIdGetter = operator.attrgetter("id"),
            items: ItemsGetterVariant = "items"
    ):
        super().__init__(text, id, item_id_getter, items)
