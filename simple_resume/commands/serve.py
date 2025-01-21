"""Contains the logic of the `serve` command."""

from __future__ import annotations

from typing import Annotated

from typer import (
    Option,
)

from simple_resume.helpers.cli import get_language, get_template
from simple_resume.helpers.constants import DEFAULT_PORT, SAMPLE_RESUME_PATH
from simple_resume.helpers.json_resume import read_and_validate_resume
from simple_resume.helpers.serve import serve_resume_for_development
from simple_resume.type_definitions.cli import (
    ResumeLanguage,
    ResumePathWithFallback,
    ResumeTemplate,
)


def serve(
    resume_path: ResumePathWithFallback = None,
    template: ResumeTemplate = None,
    language: ResumeLanguage = None,
    port: Annotated[
        int,
        Option(
            help=(
                f"The port on which the server should listen. Defaults to port {DEFAULT_PORT} if "
                "not provided."
            )
        ),
    ] = DEFAULT_PORT,
) -> None:
    """Start a web server that hosts a JSON resume."""
    resume = read_and_validate_resume(resume_path or str(SAMPLE_RESUME_PATH))
    simple_resume_metadata = resume.meta.simple_resume
    serve_resume_for_development(
        resume,
        template=get_template(simple_resume_metadata, template),
        language=get_language(simple_resume_metadata, language),
        port=port,
    )
