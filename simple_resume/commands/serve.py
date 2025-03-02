"""Contains the logic of the `serve` command."""

from __future__ import annotations

from simple_resume.helpers.constants import DEFAULT_PORT, SAMPLE_RESUME_PATH
from simple_resume.helpers.json_resume import read_and_validate_resume
from simple_resume.helpers.serve import serve_resume_for_development
from simple_resume.type_definitions.cli import (
    ResumeLanguage,
    ResumePathWithFallback,
    ResumeTemplate,
    ServerPort,
)


def serve(
    resume_path: ResumePathWithFallback = None,
    template: ResumeTemplate = None,
    language: ResumeLanguage = None,
    port: ServerPort = DEFAULT_PORT,
) -> None:
    """Start a web server that hosts a JSON resume."""
    resume = read_and_validate_resume(
        resume_path or str(SAMPLE_RESUME_PATH),
        cli_overrides={"template": template, "language": language},
    )

    serve_resume_for_development(resume, port=port)
