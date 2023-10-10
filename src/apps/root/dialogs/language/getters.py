from typing import Dict, Any

from aiogram_dialog import DialogManager

from src.utils.language import get_languages


async def languages_getter(dialog_manager: DialogManager, **_kwargs) -> Dict[str, Any]:
    l10ns = dialog_manager.middleware_data.get("l10ns")

    if not l10ns:
        return {}

    current_language = get_languages(dialog_manager.middleware_data.get("current_language"))
    languages = [language for language in get_languages(*l10ns.keys()) if language.code != current_language.locale]

    return {
        "languages": languages,
        "curr_lang_name": current_language.name,
        "curr_lang_emoji": current_language.emoij
    }


__all__ = (
    "languages_getter",
)
