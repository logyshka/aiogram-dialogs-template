from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.internal import Widget


async def on_lang_selected(call: CallbackQuery, _widget: Widget, manager: DialogManager, language: str):
    user = manager.middleware_data["user"]
    user.language = language
    await user.save()

    i18n = manager.middleware_data["l10ns"][language].format_value

    await call.answer(i18n("language-changed"), True)
    await call.message.delete()
    await manager.done()


__all__ = (
    "on_lang_selected",
)
