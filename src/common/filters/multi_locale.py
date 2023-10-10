from aiogram.filters import Filter


class MultiLocaleFilter(Filter):
    async def __call__(self, *args, **kwargs):
        return kwargs.get("l10ns") is not None
