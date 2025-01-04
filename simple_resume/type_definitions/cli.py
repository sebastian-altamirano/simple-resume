"""Contains type definitions related to the CLI."""

from __future__ import annotations

from typing import Annotated

from typer import Option

from simple_resume.helpers.constants import DEFAULT_LANGUAGE

ResumePath = Annotated[str, Option(help="The path to the JSON Resume file.")]


ResumeTemplate = Annotated[
    str | None,
    Option(
        help=(
            "The name of the template to use. If not provided, the template specified in the "
            "resume metadata will be used, or the default template ({DEFAULT_TEMPLATE}) if none is "
            "specified."
        )
    ),
]

ResumeLanguage = Annotated[
    str | None,
    Option(
        help=(
            "The language tag of the language to use, for example: 'en', 'en_US'. If not provided, "
            "the language specified in the resume metadata will be used, or the default language "
            f"({DEFAULT_LANGUAGE}) if none is specified."
        )
    ),
]

ResumeOutputPath = Annotated[
    str | None,
    Option(
        help=(
            "The path to the directory where the resume will be exported. If not provided, it will "
            "be saved to the desktop."
        )
    ),
]
