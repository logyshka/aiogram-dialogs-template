import asyncio
import logging

import coloredlogs

from src.apps import (root, )
from src.data.config import parse_config
from src.data.const import *
from src.database import init_database


async def main():
    coloredlogs.install(level=logging.INFO)
    config = parse_config(config_file=CONFIG_FILE)

    await init_database(config)

    # Запуск главного приложения.
    await root.app.start(
        bot_token=config.app_root.bot_token,
        context={
            "config": config
        },
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped!")
