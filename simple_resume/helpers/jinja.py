"""Contains helpers to work with Jinja."""

from __future__ import annotations

from typing import TYPE_CHECKING

from simple_resume.helpers.jinja_filters import get_all_custom_filters

if TYPE_CHECKING:
    from gettext import NullTranslations

    from jinja2 import Environment as JinjaEnvironment


def add_custom_filters_to_jinja_environment(
    environment: JinjaEnvironment,
    language: str,
    translations: NullTranslations,
) -> None:
    """Add custom filters to a Jinja environment.

    Args:
        environment: The Jinja environment to modify.
        language: The language to use for localization.
        translations: The message catalog to use.
    """
    environment.filters.update(get_all_custom_filters(language, translations))


def add_i18n_support_to_jinja_environment(
    environment: JinjaEnvironment, translations: NullTranslations
) -> None:
    """Add i18n support to a Jinja environment.

    Args:
        environment: The Jinja environment to modify.
        translations: The message catalog to install.
    """
    environment.add_extension("jinja2.ext.i18n")
    environment.install_gettext_translations(translations)  # pyright: ignore [reportUnknownMemberType, reportAttributeAccessIssue] (https://github.com/pallets/jinja/issues/1652)
