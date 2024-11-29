"""Contains helpers to export a JSON Resume."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from babel.support import Translations
from playwright.sync_api import sync_playwright

from simple_resume.helpers.constants import TRANSLATIONS_PATH
from simple_resume.helpers.serve import serve_resume
from simple_resume.helpers.string import remove_accents

if TYPE_CHECKING:
    from gettext import NullTranslations

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
    server = serve_resume(resume, template=template, language=language)

    # Create the output directory if it doesn't exist.
    output_path.mkdir(parents=True, exist_ok=True)

    translations = Translations.load(TRANSLATIONS_PATH, language)
    file_name = f"{get_localized_file_name_without_extension(resume, translations)}.pdf"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(server["url"])
        page.pdf(
            format="A4",
            path=output_path / file_name,
            print_background=True,
        )
        browser.close()

    server["process"].terminate()


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
