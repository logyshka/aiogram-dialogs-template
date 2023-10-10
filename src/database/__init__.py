import contextlib
import logging
import shutil

from aerich import Command
from click import Abort
from tortoise import Tortoise

from src.data.config import Config
from src.data.const import DATABASE_FILE, MIGRATION_DIR
from .api import *
from .enums import *


def prepare_orm():
    if not DATABASE_FILE.exists() and MIGRATION_DIR.exists():
        shutil.rmtree(MIGRATION_DIR, True)
        logging.info("Previous migrations were deleted")


async def init_models(tortoise_config: dict):
    command = Command(
        tortoise_config=tortoise_config,
        app="models",
        location=str(MIGRATION_DIR)
    )
    try:
        await command.init()
        await command.init_db(safe=True)
        await command.upgrade(True)
    except FileExistsError:
        await command.init()
        with contextlib.suppress(Abort):
            await command.migrate()
        await command.upgrade(True)


async def init_orm(tortoise_config: dict) -> None:
    await Tortoise.init(config=tortoise_config)
    logging.info(f"Tortoise-ORM started, {Tortoise.apps}")


async def close_orm() -> None:
    await Tortoise.close_connections()
    logging.info("Tortoise-ORM shutdown")


async def create_static_orm(config: Config):
    await User.create_static(config=config)


async def init_database(config: Config):
    prepare_orm()
    tortoise_config = config.database.get_tortoise_config(DATABASE_FILE)
    await init_orm(tortoise_config)
    await init_models(tortoise_config)
    await create_static_orm(config)


__all__ = (
    "init_database",
    "close_orm",
    "User",
    "UserRole",
)
