from dataclasses import dataclass
from typing import Union, Optional

from _decimal import Decimal

from .validator import Validator


Number = Union[int, float, Decimal]


@dataclass
class RangeValidator(Validator[Number]):
    min_value: Optional[Number] = None
    max_value: Optional[Number] = None
    min_value_error: Optional[str] = None
    max_value_error: Optional[str] = None
    any_error: Optional[str] = None

    def validate(self, value: Number) -> Number:
        if self.min_value:
            if self.min_value > value:
                raise ValueError(self.min_value_error or self.any_error)

        if self.max_value:
            if self.max_value < value:
                raise ValueError(self.max_value_error or self.any_error)

        return Number
