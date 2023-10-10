from tortoise.fields import *
from tortoise.models import Model

from .enums import *


class User(Model):
    id = IntField(pk=True)
    role = CharEnumField(UserRole)
    username = CharField(max_length=32, null=True)
    language = CharField(max_length=3, default="ru")


__all__ = (
    "User",
)
