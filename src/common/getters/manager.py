import operator
from typing import Union

from aiogram_dialog import DialogManager

from .field import GetterField
from .getter import Getter


class DialogManagerDataGetter(Getter):
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



