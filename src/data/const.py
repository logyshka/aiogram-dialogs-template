from pytz import utc
from pathlib import Path
from aiogram.enums import ParseMode


ROOT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = ROOT_DIR / "src"
DIALOGS_DIR = SRC_DIR / "dialogs"
STORAGE_DIR = SRC_DIR / "data" / "storage"
STATIC_DIR = STORAGE_DIR / "static"
BACKUP_DIR = STORAGE_DIR / "backup"
BACKUP_SUMMARY_FILE = BACKUP_DIR / "backup.zip"

CONFIG_FILE = ROOT_DIR / "config.toml"
CONFIG_BACKUP_FILE = BACKUP_DIR / CONFIG_FILE.name

DATABASE_DIR = STORAGE_DIR / "database"
MIGRATION_DIR = DATABASE_DIR / "migrations"
DATABASE_FILE = DATABASE_DIR / "database.sqlite"
DATABASE_BACKUP_FILE = BACKUP_DIR / DATABASE_FILE.name
APPS_DIR = SRC_DIR / "apps"
LOCALES_PATH = SRC_DIR / "services" / "localization" / "languages"

BOT_PARSE_MODE = ParseMode.HTML
TZ_INFO = utc


__all__ = (
    "APPS_DIR",
    "DIALOGS_DIR",
    "BACKUP_DIR",
    "BACKUP_SUMMARY_FILE",
    "CONFIG_FILE",
    "CONFIG_BACKUP_FILE",
    "STORAGE_DIR",
    "DATABASE_DIR",
    "MIGRATION_DIR",
    "DATABASE_FILE",
    "DATABASE_BACKUP_FILE",
    "BOT_PARSE_MODE",
    "STATIC_DIR",
    "TZ_INFO",
    "LOCALES_PATH"
)
