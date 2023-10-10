import operator
from dataclasses import dataclass
from typing import Optional, Any, Union

from aiogram_dialog import DialogManager


@dataclass
class GetterField:
    name: str
    result_name: Optional[str] = None
    default_value: Optional[Any] = None


class DialogManagerDataGetter:
    def __init__(self, section_name: str, *fields: Union[str, GetterField]) -> None:
        self.fields = []

        for field in fields:
            if isinstance(field, GetterField):
                self.fields.append(field)
            elif isinstance(field, str):
                self.fields.append(GetterField(name=field))

        self.section_name = section_name

    async def __call__(self, dialog_manager: DialogManager, **kwargs) -> dict:
        data = {}

        section = operator.attrgetter(self.section_name)(dialog_manager)

        for field in self.fields:
            data[field.result_name or field.name] = section.get(field.name) or field.default_value

        return data


class DialogDataGetter(DialogManagerDataGetter):
    def __init__(self, *fields: Union[str, GetterField]) -> None:
        super().__init__("dialog_data", *fields)


class StartDataGetter(DialogManagerDataGetter):
    def __init__(self, *fields: Union[str, GetterField]) -> None:
        super().__init__("start_data", *fields)


class MiddlewareDataGetter(DialogManagerDataGetter):
    def __init__(self, *fields: Union[str, GetterField]) -> None:
        super().__init__("middleware_data", *fields)


class StaticDataGetter:

    def __init__(self, **values: Any) -> None:
        self.values = values

    async def __call__(self, **kwargs) -> dict:
        return self.values


class GetterUnion:
    def __init__(self, *getters):
        self._getters = getters

    async def __call__(self, **kwargs):
        result = {}

        for getter in self._getters:
            result.update(await getter(**kwargs))

        return result


__all__ = (
    "DialogDataGetter",
    "StartDataGetter",
    "MiddlewareDataGetter",
    "StaticDataGetter",
    "GetterUnion",
    "GetterField"
)
