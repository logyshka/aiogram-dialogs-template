import re
from dataclasses import dataclass
from typing import Union, Pattern, Optional

from .validator import Validator


@dataclass
class RegexValidator(Validator[str]):
    pattern: Union[str, Pattern]
    error: Optional[str] = None

    def validate(self, value: str) -> str:
        if isinstance(self.pattern, Pattern):
            self.pattern = re.compile(self.pattern)

        if self.pattern.match(value):
            raise ValueError(self.error)

        return value
