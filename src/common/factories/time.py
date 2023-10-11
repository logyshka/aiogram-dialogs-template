from dataclasses import dataclass
from typing import Optional

from src.common.validators import RangeValidator, RegexValidator
from .factory import Factory


@dataclass
class Time:
    hours: int
    minutes: int


class TimeFactory(Factory[Time]):
    def __init__(
            self,
            hours_error: Optional[str] = None,
            minutes_error: Optional[str] = None,
            incorrect_format_error: Optional[str] = None,
    ):
        self.hours_validator = RangeValidator(min_value=0, max_value=24, any_error=hours_error)
        self.minutes_validator = RangeValidator(min_value=0, max_value=60, any_error=minutes_error)
        self.format_validator = RegexValidator(r"^\d{2}:\d{2}$", error=incorrect_format_error)

    def __call__(self, value: str) -> Time:
        self.format_validator.validate(value)

        hours, minutes = value.split(":")
        hours = self.hours_validator.validate(int(hours))
        minutes = self.minutes_validator.validate(int(minutes))

        return Time(hours, minutes)
