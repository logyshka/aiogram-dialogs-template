from typing import Union, Optional

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from src.database import User, UserRole


class UserRoleFilter(Filter):

    def __init__(self, *roles: UserRole, contains: bool = True):
        self.roles = roles
        self.contains = contains

    async def __call__(self, event: Union[Message, CallbackQuery], user: Optional[User]) -> bool:
        if not user:
            return False

        contains = user.role in self.roles

        if self.contains:
            return contains
        return not contains
