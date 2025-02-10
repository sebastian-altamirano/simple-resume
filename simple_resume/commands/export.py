"""Contains the logic of the `export` command."""

from __future__ import annotations

from typer import BadParameter

from simple_resume.helpers.cli import get_language, get_output_path, get_template
from simple_resume.helpers.export import export_resume
from simple_resume.helpers.i18n import get_translations
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

    resume = read_and_validate_resume(resume_path)
    simple_resume_metadata = resume.meta.simple_resume
    final_template = get_template(simple_resume_metadata, template)
    final_language = get_language(simple_resume_metadata, language)
    final_output_path = get_output_path(output_path)

    export_resume(
        resume,
        template=final_template,
        language=final_language,
        output_path=final_output_path,
        translations=get_translations(final_language),
        browser_channel=browser_channel,
        should_install_browser=should_install_browser,
    )
