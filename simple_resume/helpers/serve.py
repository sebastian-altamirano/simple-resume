"""Contains helpers to serve a JSON Resume."""

from __future__ import annotations

from typing import TYPE_CHECKING

from babel.support import Translations
from flask import Flask, render_template

from simple_resume.helpers.constants import TEMPLATES_PATH, TRANSLATIONS_PATH
from simple_resume.helpers.jinja import (
    add_custom_filters_to_jinja_environment,
    add_i18n_support_to_jinja_environment,
)

if TYPE_CHECKING:
    from simple_resume.type_definitions.json_resume import JsonResume


def serve_resume(
    resume: JsonResume,
    template: str,
    language: str,
) -> None:
    """Serve a JSON Resume.

    Args:
        resume: The content of a JSON Resume file.
        template: The name of the template to use.
        language: The language tag of the language to use.
    """
    template_path = TEMPLATES_PATH / template
    app = Flask(
        __name__,
        static_folder=(template_path / "static").as_posix(),
        template_folder=template_path.as_posix(),
    )

    add_custom_filters_to_jinja_environment(app.jinja_env, language)
    translations = Translations.load(TRANSLATIONS_PATH, language)
    add_i18n_support_to_jinja_environment(app.jinja_env, translations)

    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    app.add_url_rule("/", "index", lambda: render_template("index.jinja", **resume))

    app.run(debug=True)
