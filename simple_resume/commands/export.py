"""Contains the logic of the `export` command."""

from __future__ import annotations

from pathlib import Path

from typer import BadParameter

from simple_resume.helpers.constants import DEFAULT_OUTPUT_PATH
from simple_resume.helpers.export import export_resume
from simple_resume.helpers.json_resume import read_and_validate_resume
from simple_resume.type_definitions.cli import (
    BrowserChannel,
    ResumeLanguage,
    ResumeOutputPath,
    ResumePath,
    ResumeTemplate,
    ShouldInstallBrowser,
)
from simple_resume.type_definitions.export import SupportedBrowserChannel


def _get_output_path(output_path: str | None) -> Path:
    """Resolve the output path or return the default one.

    Args:
        output_path: The output path specified via CLI argument.

    Returns:
        The determined output path.
    """
    return (output_path is not None and Path(output_path).resolve()) or DEFAULT_OUTPUT_PATH


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


def export(
    resume_path: ResumePath,
    template: ResumeTemplate = None,
    language: ResumeLanguage = None,
    output_path: ResumeOutputPath = None,
    browser_channel: BrowserChannel = None,
    *,
    should_install_browser: ShouldInstallBrowser = False,
) -> None:
    """Export a JSON resume."""
    _validate_should_install_browser(browser_channel, should_install_browser=should_install_browser)

    resume = read_and_validate_resume(
        resume_path, cli_overrides={"template": template, "language": language}
    )
    export_resume(
        resume,
        output_path=_get_output_path(output_path),
        browser_channel=browser_channel,
        should_install_browser=should_install_browser,
    )
