from tortoise.expressions import *
from tortoise.queryset import QuerySet

from src.data.config import Config
from .enums import *
from .models import *


class User(User):
    @classmethod
    async def register(cls, config: Config, user_id: int, username: str) -> "User":
        user = await cls.get_or_none(id=user_id)

        if user:
            return user

        if user_id == config.main_app.owner_id:
            role = UserRole.OWNER
        elif user_id in config.main_app.admin_ids:
            role = UserRole.ADMIN
        else:
            role = UserRole.USER

        return await cls.create(
            id=user_id,
            username=username,
            role=role
        )

    @classmethod
    async def create_static(cls, config: Config) -> None:
        for admin_id in [*config.main_app.admin_ids, config.main_app.owner_id]:
            await cls.register(config, admin_id, "")

    @classmethod
    async def search_user(cls, user_id: Union[str, int]) -> Optional["User"]:
        try:
            if user_id[0] == "@":
                user = await User.get_or_none(username=user_id[1:])
            else:
                user = await User.get_or_none(id=user_id[1:])
            return user
        except Exception:
            return None

    @classmethod
    def get_all(cls) -> QuerySet["User"]:
        return cls.filter()

    @classmethod
    def get_admins(cls) -> QuerySet["User"]:
        return cls.filter(Q(role=UserRole.ADMIN) | Q(role=UserRole.OWNER))

    async def update(self, **kwargs) -> None:
        await self.filter(id=self.id).update(**kwargs)


__all__ = (
    "User",
)
