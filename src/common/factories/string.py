from dataclasses import dataclass
from typing import Optional

from .factory import Factory
from ..validators import RangeValidator, RegexValidator


@dataclass
class StringFactory(Factory[str]):
    length_validator: Optional[RangeValidator] = None
    regex_validator: Optional[RegexValidator] = None

    def __call__(self, value: str) -> str:
        if self.length_validator:
            self.length_validator.validate(len(value))

        if self.regex_validator:
            self.regex_validator.validate(value)

        return value
