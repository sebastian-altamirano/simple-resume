"""Contains helpers to export a JSON Resume."""

from __future__ import annotations

from typing import TYPE_CHECKING

import jinja2
from babel.support import Translations
from weasyprint import HTML

from simple_resume.helpers.constants import TEMPLATES_PATH, TRANSLATIONS_PATH
from simple_resume.helpers.jinja import (
    add_custom_filters_to_jinja_environment,
    add_i18n_support_to_jinja_environment,
)
from simple_resume.helpers.string import remove_accents

if TYPE_CHECKING:
    from gettext import NullTranslations
    from pathlib import Path

    from simple_resume.type_definitions.json_resume import JsonResume


def export_resume(
    resume: JsonResume,
    template: str,
    language: str,
    output_path: Path,
) -> None:
    """Export a JSON Resume.

    Args:
        resume: The content of a JSON Resume file.
        template: The name of the template to use.
        language: The language tag of the language to use.
        output_path: The path to the directory where the resume will be exported.
    """
    environment = jinja2.Environment(
        autoescape=jinja2.select_autoescape(),
        loader=jinja2.FileSystemLoader(TEMPLATES_PATH / template),
    )
    add_custom_filters_to_jinja_environment(environment, language)
    translations = Translations.load(TRANSLATIONS_PATH, language)
    add_i18n_support_to_jinja_environment(environment, translations)

    compiled_template = environment.get_template("index.jinja").render(resume)

    # Create the output directory if it doesn't exist.
    output_path.mkdir(parents=True, exist_ok=True)

    HTML(string=compiled_template).write_pdf(  # pyright: ignore [reportUnknownMemberType]
        output_path / f"{get_localized_file_name_without_extension(resume, translations)}.pdf"
    )


def get_localized_file_name_without_extension(
    resume: JsonResume, translations: NullTranslations
) -> str:
    """Return the localized file name of a JSON Resume without extension.

    Args:
        resume: The content of a JSON Resume file.
        translations: The message catalog to use.

    Returns:
        The localized file name without extension.
    """
    name = resume.get("basics", {}).get("name", translations.gettext("Anonymous"))
    formatted_name = "_".join(remove_accents(name).split(" "))
    return translations.gettext("{name}_Resume").format(name=formatted_name)
