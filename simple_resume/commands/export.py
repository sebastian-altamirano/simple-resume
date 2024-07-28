"""Contains the logic of the `export` command."""

from __future__ import annotations

from simple_resume.helpers.cli import get_language, get_output_path, get_template
from simple_resume.helpers.export import export_resume
from simple_resume.helpers.json_resume import get_simple_resume_metadata, read_and_validate_resume
from simple_resume.type_definitions.cli import (  # noqa: TCH001 Typer requires these type annotations to be available at runtime.
    ResumeLanguage,
    ResumeOutputPath,
    ResumePath,
    ResumeTemplate,
)


def export(
    resume_path: ResumePath,
    template: ResumeTemplate = None,
    language: ResumeLanguage = None,
    output_path: ResumeOutputPath = None,
) -> None:
    """Export a JSON resume."""
    resume = read_and_validate_resume(resume_path)
    metadata = get_simple_resume_metadata(resume)
    export_resume(
        resume,
        template=get_template(metadata, template),
        language=get_language(metadata, language),
        output_path=get_output_path(output_path),
    )
