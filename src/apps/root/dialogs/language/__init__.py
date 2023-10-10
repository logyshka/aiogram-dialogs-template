import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format

from src.common.widgets import I18NFormat, Close
from src.apps.root.states import LanguageDialog
from .functions import *
from .getters import *

dialog = Dialog(
    Window(
        I18NFormat("language-root"),
        Select(
            id="language",
            item_id_getter=operator.attrgetter("code"),
            items="languages",
            text=Format("{item.label}"),
            on_click=on_lang_selected
        ),
        Close(I18NFormat("close")),
        state=LanguageDialog.root,
        getter=languages_getter
    )
)
