"""Contains helpers to export a JSON Resume."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import flask.cli
from playwright.sync_api import sync_playwright
from portpicker import pick_unused_port

from simple_resume.helpers.cli_logging import (
    print_error_message,
    print_info_message,
    print_success_message,
)
from simple_resume.helpers.i18n import get_localized_file_name_without_extension, get_translations
from simple_resume.helpers.playwright import launch_browser
from simple_resume.helpers.serve import serve_resume_for_export
from simple_resume.type_definitions.export import SupportedBrowserChannel, SupportedPaperSize

if TYPE_CHECKING:
    from pathlib import Path

    from simple_resume.models.json_resume import JsonResume


def export_resume(
    resume: JsonResume,
    output_path: Path,
    paper_size: SupportedPaperSize,
    browser_channel: SupportedBrowserChannel | None,
    *,
    should_install_browser: bool,
) -> None:
    """Export a JSON Resume.

    Args:
        resume: A validated JSON Resume.
        output_path: The path to the directory where the resume will be exported.
        paper_size: The paper size to use for the PDF.
        browser_channel: The browser to use to generate the PDF file. If `None`, it will try to use
            a browser installed in the system.
        should_install_browser: Whether to install the specified browser if it is not already
            installed.

    Raises:
        BrowserNotFoundError: If no compatible browser is available.
        KeyboardInterrupt: If the browser installation is interrupted.
        subprocess.CalledProcessError: If the browser installation fails.
    """
    # Disable all Flask logging.
    flask.cli.show_server_banner = lambda *_args: None  # type: ignore
    logging.getLogger("werkzeug").disabled = True

    print_info_message("Exporting the resume...")
    port = pick_unused_port()
    serve_resume_for_export(resume, port=port)

    try:
        # Create the output directory if it doesn't exist.
        output_path.mkdir(parents=True, exist_ok=True)

        translations = get_translations(resume.meta.simple_resume.language)
        file_name = f"{get_localized_file_name_without_extension(resume, translations)}.pdf"
        resume_path = output_path / file_name

        _generate_pdf(
            f"http://localhost:{port}",
            resume_path,
            paper_size,
            browser_channel,
            should_install_browser=should_install_browser,
        )
        print_success_message(f"Resume exported to `{resume_path}`.")
    except:
        print_error_message("Failed to export the resume.")
        raise


def _generate_pdf(
    server_url: str,
    resume_path: Path,
    paper_size: SupportedPaperSize,
    browser_channel: SupportedBrowserChannel | None,
    *,
    should_install_browser: bool,
) -> None:
    """Generate a PDF from a JSON Resume that is being served.

    Args:
        server_url: The URL of the server where the resume is being served.
        resume_path: The path where the generated PDF will be saved.
        paper_size: The paper size to use for the PDF.
        browser_channel: The browser to use to generate the PDF file. If `None`, it will try to use
            a browser installed in the system.
        should_install_browser: Whether to install the specified browser if it is not already
            installed.

    Raises:
        BrowserNotFoundError: If no compatible browser is available.
        KeyboardInterrupt: If the browser installation is interrupted.
        subprocess.CalledProcessError: If the browser installation fails.
    """
    with sync_playwright() as playwright:
        browser = launch_browser(
            playwright, browser_channel=browser_channel, should_install=should_install_browser
        )
        page = browser.new_page()
        page.goto(server_url, wait_until="load")
        page.pdf(
            path=resume_path,
            print_background=True,
            format=paper_size,
        )
        browser.close()
