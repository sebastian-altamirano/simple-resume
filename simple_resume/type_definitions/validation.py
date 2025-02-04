"""Contains type definitions related to the validation process."""

from __future__ import annotations

from typing import TypeVar

from pydantic import HttpUrl
from pydantic_extra_types.language_code import LanguageAlpha2

JsonSchemaUrl = TypeVar("JsonSchemaUrl", bound=HttpUrl | None)
ResumeLanguage = TypeVar("ResumeLanguage", bound=LanguageAlpha2 | None)
ResumeTemplate = TypeVar("ResumeTemplate", bound=str | None)
