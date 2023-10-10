import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from re import Pattern
from typing import Generic, TypeVar, Union, Iterable

from _decimal import Decimal
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

T = TypeVar("T")
Number = Union[int, float, Decimal]
Regex = Union[Pattern, str]


@dataclass
class Time:
    hours: int
    minutes: int


class Factory(ABC, Generic[T]):
    @abstractmethod
    def __call__(self, value: str) -> T:
        pass

    @staticmethod
    async def on_error(msg: Message, _widget: TextInput, _manager: DialogManager, error: ValueError):
        error = str(error) or "неизвестная ошибка"
        await msg.reply(f"<b>⚠️ Произошла ошибка:</b> <code>{error}</code>")


class NumberFactory(Factory[Number]):
    def __init__(self, min_value: Number = None, max_value: Number = None):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, value: str) -> Number:
        result = int(value)
        if type(self.min_value) == type(result):
            if self.min_value < result:
                raise ValueError(f"введённое число должно быть больше, чем {self.min_value}")
        if type(self.max_value) == type(result):
            if self.max_value > result:
                raise ValueError(f"введённое число должно быть меньше, чем {self.max_value}")
        return result


class StringFactory(Factory[str]):
    def __init__(
            self,
            min_length: int = None,
            max_length: int = None,
            banned_chars: Iterable[str] = None,
            regex: Regex = None
    ):
        self.length_factory = NumberFactory(
            min_value=min_length,
            max_value=max_length
        )
        self.banned_chars = banned_chars
        self.regex = regex

        if isinstance(self.regex, str):
            self.regex = re.compile(self.regex)

    def __call__(self, value: str) -> str:
        try:
            self.length_factory(len(value))
        except ValueError:
            raise ValueError("некорректная длина строки")
        if self.banned_chars:
            for char in self.banned_chars:
                if char in value:
                    raise ValueError(f"в строке запрещённый символ '{char}'")
        if self.regex:
            if not self.regex.match(value):
                raise ValueError("строка не соответствует шаблону")
        return value


class TimeFactory(Factory[Time]):
    def __init__(self):
        self.hours_factory = NumberFactory(min_value=0, max_value=24)
        self.minutes_factory = NumberFactory(min_value=0, max_value=60)

    def __call__(self, value: str) -> Time:
        if ":" not in value:
            raise ValueError("некорректный формат времени")
        hours, minutes = value.split(":")
        try:
            return Time(
                hours=self.hours_factory(hours),
                minutes=self.minutes_factory(minutes)
            )
        except ValueError:
            raise ValueError("некорректное время")


class UsernameFactory(StringFactory):
    def __init__(self):
        super().__init__(
            max_length=33,
            regex=r"^@[a-zA-Z\d]+$"
        )


class IDFactory(StringFactory):
    def __init__(self):
        super().__init__(
            regex=r"#\d+",
            max_length=20
        )


__all__ = (
    "NumberFactory",
    "StringFactory",
    "TimeFactory",
    "IDFactory",
    "UsernameFactory"
)
