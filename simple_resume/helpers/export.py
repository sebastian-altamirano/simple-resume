"""Contains helpers to export a JSON Resume."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import flask.cli
from babel.support import Translations
from playwright.sync_api import sync_playwright

from simple_resume.helpers.constants import DEFAULT_PORT, TRANSLATIONS_PATH
from simple_resume.helpers.i18n import get_localized_file_name_without_extension
from simple_resume.helpers.logging import (
    print_error_message,
    print_info_message,
    print_success_message,
)
from simple_resume.helpers.serve import serve_resume_for_export

if TYPE_CHECKING:
    from pathlib import Path

    from simple_resume.models.json_resume import JsonResume


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
    # Disable all Flask logging.
    flask.cli.show_server_banner = lambda *_args: None  # type: ignore
    logging.getLogger("werkzeug").disabled = True

    print_info_message("Exporting the resume...")
    server = serve_resume_for_export(
        resume, template=template, language=language, port=DEFAULT_PORT
    )

    try:
        # Create the output directory if it doesn't exist.
        output_path.mkdir(parents=True, exist_ok=True)

        translations = Translations.load(TRANSLATIONS_PATH, language)
        file_name = f"{get_localized_file_name_without_extension(resume, translations)}.pdf"
        resume_path = output_path / file_name

        _generate_pdf(f"http://localhost:{DEFAULT_PORT}", resume_path)
        print_success_message(
            f"Resume exported to `{resume_path}` (language: {language}; template: {template})."
        )
    except:
        print_error_message("Failed to export the resume.")
        raise
    finally:
        server.terminate()


def _generate_pdf(server_url: str, resume_path: Path) -> None:
    """Generate a PDF from a JSON Resume that is being served.

    Args:
        server_url: The URL of the server where the resume is being served.
        resume_path: The path where the generated PDF will be saved.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            channel="chromium",
        )
        page = browser.new_page()
        page.goto(server_url, wait_until="load")
        page.pdf(
            path=resume_path,
            prefer_css_page_size=True,
            print_background=True,
        )
        browser.close()
