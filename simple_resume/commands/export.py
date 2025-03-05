"""Contains the logic of the `export` command."""

from __future__ import annotations

from pathlib import Path

from typer import BadParameter

from simple_resume.helpers.constants import DEFAULT_OUTPUT_PATH
from simple_resume.helpers.export import export_resume
from simple_resume.helpers.json_resume import read_and_validate_resume
from simple_resume.type_definitions.cli import (
    BrowserChannel,
    PaperSize,
    ResumeLanguage,
    ResumeOutputPath,
    ResumePath,
    ResumeTemplate,
    ShouldInstallBrowser,
)
from simple_resume.type_definitions.export import SupportedBrowserChannel


def _validate_should_install_browser(
    browser_channel: SupportedBrowserChannel | None, *, should_install_browser: bool
) -> None:
    """Validate `--install-browser`.

    Args:
        browser_channel: The value of `--browser`.
        should_install_browser: The value of `--install-browser`.

    Raises:
        typer.BadParameter: If `--install-browser` is `True` and `--browser` is not specified.
    """
    if should_install_browser and not browser_channel:
        raise BadParameter("`--install-browser` requires `--browser` to be specified.")


def export(  # noqa: PLR0913
    resume_path: ResumePath,
    template: ResumeTemplate = None,
    language: ResumeLanguage = None,
    output_path: ResumeOutputPath = str(DEFAULT_OUTPUT_PATH),
    paper_size: PaperSize = None,
    browser_channel: BrowserChannel = None,
    *,
    should_install_browser: ShouldInstallBrowser = False,
) -> None:
    """Export a JSON resume."""
    _validate_should_install_browser(browser_channel, should_install_browser=should_install_browser)

    resume = read_and_validate_resume(
        resume_path,
        cli_overrides={"language": language, "paper_size": paper_size, "template": template},
    )
    export_resume(
        resume,
        output_path=Path(output_path).resolve(),
        browser_channel=browser_channel,
        should_install_browser=should_install_browser,
    )
