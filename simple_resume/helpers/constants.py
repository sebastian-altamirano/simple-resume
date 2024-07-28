"""Contains constants."""

from __future__ import annotations

from pathlib import Path

DEFAULT_LANGUAGE = "en"
DEFAULT_OUTPUT_PATH = Path("~/Desktop").expanduser()
DEFAULT_TEMPLATE = "basic"

PACKAGE_PATH = (Path(__file__) / ".." / "..").resolve()
SCHEMAS_PATH = (PACKAGE_PATH / "schemas").resolve()
TEMPLATES_PATH = (PACKAGE_PATH / "templates").resolve()
TRANSLATIONS_PATH = (PACKAGE_PATH / "translations").resolve()

JSON_RESUME_SCHEMA_PATH = (SCHEMAS_PATH / "json-resume-v1.schema.json").resolve()
JSON_RESUME_SCHEMA_URL = (
    "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json"
)
SIMPLE_RESUME_METADATA_SCHEMA_PATH = (SCHEMAS_PATH / "simple-resume-metadata.schema.json").resolve()
