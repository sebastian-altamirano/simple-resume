"""Contains helpers to work with translations."""

from __future__ import annotations

from simple_resume.helpers.constants import TRANSLATIONS_PATH


def get_supported_languages() -> list[str]:
    """Return the language tags of the supported languages."""
    return [path.name for path in TRANSLATIONS_PATH.glob("*") if path.is_dir()]
