from dataclasses import asdict
from pathlib import Path

import toml


class Storable:
    __path: Path
    __entity_to_save: "Storable" = None
    __loaded: bool = False

    def __setattr__(self, key, value) -> None:
        self.__dict__[key] = value

        if self.__loaded:
            self.__save()

    def __save(self) -> None:
        # noinspection PyDataclass
        dict_data = asdict(self.__entity_to_save)

        with open(self.__path, "w") as f:
            toml.dump(dict_data, f)

    @classmethod
    def configure_path(cls, path: Path) -> None:
        cls.__path = path

    @classmethod
    def make_loaded(cls, entity_to_save: "Storable") -> None:
        cls.__loaded = True
        cls.__entity_to_save = entity_to_save
