"""Contains the logic of the `serve` command."""

from __future__ import annotations

from simple_resume.helpers.cli import get_language, get_template
from simple_resume.helpers.json_resume import get_simple_resume_metadata, read_and_validate_resume
from simple_resume.helpers.serve import serve_resume
from simple_resume.type_definitions.cli import (  # noqa: TCH001 Typer requires these type annotations to be available at runtime.
    ResumeLanguage,
    ResumePath,
    ResumeTemplate,
)


def serve(
    resume_path: ResumePath,
    template: ResumeTemplate = None,
    language: ResumeLanguage = None,
) -> None:
    """Start a web server that hosts a JSON resume."""
    resume = read_and_validate_resume(resume_path)
    metadata = get_simple_resume_metadata(resume)
    serve_resume(
        resume, template=get_template(metadata, template), language=get_language(metadata, language)
    )
