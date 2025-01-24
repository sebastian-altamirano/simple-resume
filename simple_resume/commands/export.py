"""Contains the logic of the `export` command."""

from __future__ import annotations

from simple_resume.helpers.cli import get_language, get_output_path, get_template
from simple_resume.helpers.export import export_resume
from simple_resume.helpers.i18n import get_translations
from simple_resume.helpers.json_resume import read_and_validate_resume
from simple_resume.type_definitions.cli import (
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
    )
