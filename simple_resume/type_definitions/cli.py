"""Contains type definitions related to the CLI."""

from __future__ import annotations

from typing import Annotated, TypedDict

from typer import Argument, Option

from simple_resume.helpers.constants import DEFAULT_LANGUAGE
from simple_resume.type_definitions.export import SupportedBrowserChannel, SupportedPaperSize

ResumePath = Annotated[str, Argument(help="The path to the JSON Resume file.")]

ResumePathWithFallback = Annotated[
    str | None,
    Argument(
        help="The path to the JSON Resume file. If not provided, a sample resume will be used."
    ),
]

ResumeTemplate = Annotated[
    str | None,
    Option(
        "--template",
        "-t",
        help=(
            "The name of the template to use. If not provided, the template specified in the "
            "resume metadata will be used, or the default template ({DEFAULT_TEMPLATE}) if none is "
            "specified."
        ),
    ),
]

ResumeLanguage = Annotated[
    str | None,
    Option(
        "--language",
        "-l",
        help=(
            "The language tag of the language to use, for example: 'en', 'en_US'. If not provided, "
            "the language specified in the resume metadata will be used, or the default language "
            f"({DEFAULT_LANGUAGE}) if none is specified."
        ),
    ),
]

ResumeOutputPath = Annotated[
    str | None,
    Option(
        "--output-path",
        "-o",
        help=(
            "The path to the directory where the resume will be exported. If not provided, it will "
            "be saved to the desktop."
        ),
    ),
]


BrowserChannel = Annotated[
    SupportedBrowserChannel | None,
    Option(
        "--browser",
        "-b",
        help=(
            "The browser to use to generate the PDF. If not provided, the application will attempt "
            "to use a compatible browser. If no compatible browser is found, the process will fail."
        ),
    ),
]

ShouldInstallBrowser = Annotated[
    bool,
    Option(
        "--install-browser",
        help="Installs the browser specified with `--browser` if it is not already installed.",
    ),
]

ServerPort = Annotated[
    int,
    Option(
        "--port",
        "-p",
        help=("The port on which the server should listen."),
    ),
]

PaperSize = Annotated[
    SupportedPaperSize,
    Option(
        "--size",
        "-z",
        help=("The paper size of the PDF."),
    ),
]


class SimpleResumeMetadataCliOverrides(TypedDict):
    """CLI options that override values within the `/meta/simpleResume` section of a JSON Resume."""

    language: ResumeLanguage
    template: ResumeTemplate
