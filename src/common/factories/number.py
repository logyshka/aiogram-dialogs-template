from dataclasses import dataclass
from typing import Optional

from src.common.validators import Number, RangeValidator
from .factory import Factory


@dataclass
class NumberFactory(Factory[Number]):
    number_type: type
    range_validator: Optional[RangeValidator] = None

    def __call__(self, value: str) -> Number:
        result = self.number_type(value)

        if self.range_validator:
            self.range_validator.validate(result)
        return result
