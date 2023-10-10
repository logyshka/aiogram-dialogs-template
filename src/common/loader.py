import codecs
import logging
import os
from pathlib import Path
from typing import Any, Dict, Generator, List, Union
from typing import Optional

from aiogram import Router
from aiogram_dialog import Dialog
from fluent.runtime import FluentLocalization, FluentResourceLoader
from fluent.syntax import FluentParser
from fluent.syntax.ast import Resource

PathLike = Union[str, Path]


def validate_path(path: PathLike) -> Path:
    if isinstance(path, str):
        path = Path(path)
    if path.exists():
        return path
    raise ValueError("Path %s doesn't exists!" % path)


def make_import_path(path: Path) -> str:
    parts = []
    i = 0

    for part in path.parts:
        if i > 0 or part == "src":
            parts.append(part)
            i += 1

    return ".".join(parts)


class Loader:
    def __init__(
            self,
            app_path: PathLike,
            dialogs_path: Optional[PathLike] = None,
            routers_path: Optional[PathLike] = None,
            locales_path: Optional[PathLike] = None,
    ):
        app_path = validate_path(app_path).parent
        self.dialogs_path = validate_path(dialogs_path or app_path / "dialogs")
        self.routers_path = validate_path(routers_path or app_path / "routers")
        self.locales_path = validate_path(locales_path or app_path / "locales")

    def _get_all_of_type(self, path: Path, import_path: str, var_type: type) -> list[type]:
        result = []

        for item in path.iterdir():
            if item.is_dir():
                result += self._get_all_of_type(item, import_path + "." + item.name, var_type)
            elif item.name.endswith(".py"):
                module_name = item.name.rstrip(".py")
                module = __import__(import_path, fromlist=[module_name])

                if module_name != "__init__":
                    module = module.__dict__[module_name]

                for var_name in module.__dict__.keys():
                    if isinstance(var_name, str):
                        if not var_name.startswith("__"):
                            var_value = module.__dict__[var_name]
                            if isinstance(var_value, var_type):
                                result.append(var_value)
        return result

    def load_dialogs(self) -> list[Dialog]:
        return self._get_all_of_type(
            self.dialogs_path,
            make_import_path(self.dialogs_path),
            Dialog
        )

    def load_routers(self) -> list[Router]:
        return self._get_all_of_type(
            self.routers_path,
            make_import_path(self.routers_path),
            Router
        )

    def load_l10ns(self, default_locale: str) -> Dict[str, FluentLocalization]:
        l10ns = {}
        loader = CustomFluentResourceLoader(str(self.locales_path / "{locale}.ftl"))
        for locale_file in self.locales_path.iterdir():
            locale = locale_file.name.rstrip(".ftl")
            l10ns[locale] = FluentLocalization(
                locales=[locale, default_locale],
                resource_ids=[locale_file.name],
                resource_loader=loader
            )
        return l10ns


class CustomFluentResourceLoader(FluentResourceLoader):
    def resources(self, locale: str, resource_ids: List[str]) -> Generator[List['Resource'], None, None]:
        for root in self.roots:
            path = self.localize_path(root, locale)
            if not os.path.isfile(path):
                logging.info("File with localalization is not found: %s" % path)
                continue
            content = codecs.open(path, 'r', 'utf-8').read()
            resources = [FluentParser().parse(content)]
            if resources:
                yield resources

    def localize_path(self, path: str, locale: str) -> str:
        return path.format(locale=locale)
