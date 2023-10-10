from dataclasses import dataclass
from typing import List, Union


@dataclass
class Language:
    locale: str
    name: str
    emoij: str

    @property
    def label(self) -> str:
        return f"{self.emoij} {self.name}"


LANGUAGES = [
    Language("ru", "Русский", "🇷🇺"),
    Language("en", "English", "🇺🇸")
]


def get_languages(*locales: str) -> Union[List[Language], Language]:
    languages = []
    for locale in locales:
        for language in LANGUAGES:
            if language.locale == locale:
                languages.append(language)

    return languages[0] if len(languages) > 0 else languages
