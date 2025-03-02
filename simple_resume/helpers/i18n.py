"""Contains helpers to work with translations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from babel.support import Translations

from simple_resume.helpers.constants import TRANSLATIONS_PATH
from simple_resume.helpers.string_manipulation import remove_accents

if TYPE_CHECKING:
    from babel.support import NullTranslations

    from simple_resume.models.json_resume import JsonResume


def get_localized_file_name_without_extension(
    resume: JsonResume, translations: NullTranslations
) -> str:
    """Return the localized file name of a JSON Resume without extension.

    Args:
        resume: A validated JSON Resume.
        translations: The message catalog to use.

    Returns:
        The localized file name without extension.
    """
    name = resume.basics.name or translations.gettext("Anonymous")
    formatted_name = "_".join(remove_accents(name).split(" "))
    return translations.gettext("{name}_Resume").format(name=formatted_name)


def get_supported_languages() -> list[str]:
    """Return the language tags of the supported languages."""
    return [path.name for path in TRANSLATIONS_PATH.glob("*") if path.is_dir()]


def get_translations(language: str) -> NullTranslations:
    """Return the translations for the given language.

    Args:
        language: The language tag of the language to use.
    """
    return Translations.load(TRANSLATIONS_PATH, language)
