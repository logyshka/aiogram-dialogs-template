import logging
from dataclasses import dataclass, fields, MISSING
from pathlib import Path
from typing import *

import toml

from src.data.storable import Storable


@dataclass
class MainAppConfig(Storable):
    owner_id: int
    bot_token: str
    admin_ids: list[int]


@dataclass
class AppsConfig(Storable):
    pass


@dataclass
class DatabaseConfig(Storable):
    models: list[str]
    protocol: str
    user: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[str] = None

    def get_tortoise_config(self, database_path: str) -> dict:
        if self.protocol == "sqlite":
            db_url = f"{self.protocol}://{database_path}"
        else:
            db_url = f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}"

        return {
            "connections": {"default": db_url},
            "apps": {
                "models": {
                    "models": self.models,
                    "default_connection": "default",
                },
            },
        }


@dataclass
class Config(Storable):
    apps: AppsConfig
    main_app: MainAppConfig
    database: DatabaseConfig


def parse_config(config_file: Path) -> Config:
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file} no such file")

    Storable.configure_path(config_file)

    with open(config_file, "r") as f:
        data = toml.load(f)

    sections = {}

    for section in fields(Config):
        pre = {}

        current = data[section.name]

        for field in fields(section.type):
            if field.name in current:
                pre[field.name] = current[field.name]
            elif field.default is not MISSING:
                pre[field.name] = field.default
            else:
                raise ValueError(
                    f"Missing field {field.name} in section {section.name}"
                )

        sections[section.name] = section.type(**pre)

    config = Config(**sections)

    Storable.make_loaded(config)

    logging.info("Config was successfully parsed")

    return config


__all__ = (
    "Config",
    "parse_config",
)
