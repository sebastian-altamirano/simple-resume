"""Contains helpers to serve a JSON Resume."""

from __future__ import annotations

from multiprocessing import Process
from typing import TYPE_CHECKING

from babel.support import Translations
from flask import Flask
from jinjax import Catalog

from simple_resume.helpers.constants import (
    COMPONENTS_PATH,
    STATIC_PATH,
    TEMPLATES_PATH,
    TRANSLATIONS_PATH,
)
from simple_resume.helpers.jinja import (
    add_custom_filters_to_jinja_environment,
    add_i18n_support_to_jinja_environment,
)

if TYPE_CHECKING:
    from simple_resume.type_definitions.json_resume import JsonResume
    from simple_resume.type_definitions.serve import SimpleResumeServer


def serve_resume(resume: JsonResume, template: str, language: str) -> SimpleResumeServer:
    """Serve a JSON Resume.

    Args:
        resume: The content of a JSON Resume file.
        template: The name of the template to use.
        language: The language tag of the language to use.

    Returns:
        A process instance that can be used to stop the server.
    """
    port = 5000
    process = Process(
        target=lambda: _create_flask_app_for_resume(resume, template, language).run(port=port)
    )
    process.start()
    return {"process": process, "url": f"http://localhost:{port}"}


def _create_flask_app_for_resume(
    resume: JsonResume,
    template: str,
    language: str,
) -> Flask:
    """Create a Flask application to serve a JSON Resume.

    Args:
        resume: The content of a JSON Resume file.
        template: The name of the template to use.
        language: The language tag of the language to use.

    Returns:
        A Flask application instance configured to serve the JSON Resume.
    """
    app = Flask(__name__)

    add_custom_filters_to_jinja_environment(app.jinja_env, language)
    translations = Translations.load(TRANSLATIONS_PATH, language)
    add_i18n_support_to_jinja_environment(app.jinja_env, translations)

    catalog = Catalog(jinja_env=app.jinja_env, root_url="/static/")
    catalog.add_folder(COMPONENTS_PATH)
    catalog.add_folder(TEMPLATES_PATH / template)
    catalog.add_folder(STATIC_PATH)
    app.wsgi_app = catalog.get_middleware(
        app.wsgi_app, autorefresh=app.debug, allowed_ext=[".css", ".svg", ".woff", ".woff2"]
    )

    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    app.add_url_rule("/", "index", lambda: catalog.render("Resume", **resume))

    return app
