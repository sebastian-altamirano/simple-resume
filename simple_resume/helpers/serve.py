"""Contains helpers to serve a JSON Resume."""

from __future__ import annotations

from multiprocessing import Process
from typing import TYPE_CHECKING

from babel.support import Translations
from flask import Flask
from jinjax import Catalog
from livereload import Server

from simple_resume.helpers.constants import (
    COMPONENTS_PATH,
    STATIC_PATH,
    TEMPLATES_PATH,
    TRANSLATIONS_PATH,
)
from simple_resume.helpers.i18n import get_localized_file_name_without_extension
from simple_resume.helpers.jinja import (
    add_custom_filters_to_jinja_environment,
    add_i18n_support_to_jinja_environment,
)

if TYPE_CHECKING:
    from simple_resume.type_definitions.json_resume import JsonResume


def serve_resume_for_development(
    resume: JsonResume, template: str, language: str, port: int
) -> None:
    """Serve a JSON Resume with live reloading.

    Args:
        resume: The content of a JSON Resume file.
        template: The name of the template to use.
        language: The language tag of the language to use.
        port: The port on which the server should listen.
    """
    app = _create_flask_app_for_resume(resume, template, language)
    app.debug = True

    server = Server(app.wsgi_app)
    server.watch("**/*.jinja")
    server.watch("**/*.css")
    server.watch("**/*.js")

    server.serve(port=port)


def serve_resume_for_export(resume: JsonResume, template: str, language: str, port: int) -> Process:
    """Serve a JSON Resume without live reloading and wrapped in a process, so it can be stopped.

    Args:
        resume: The content of a JSON Resume file.
        template: The name of the template to use.
        language: The language tag of the language to use.
        port: The port on which the server should listen.

    Returns:
        A process instance that can be used to stop the server.
    """
    app = _create_flask_app_for_resume(resume, template, language)

    port = 5000
    process = Process(target=lambda: app.run(port=port))
    process.start()

    return process


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

    # Auto-reload is disabled because it is handled by the livereload server.
    auto_reload = False
    app.jinja_env.auto_reload = auto_reload
    app.config["TEMPLATES_AUTO_RELOAD"] = auto_reload

    catalog = Catalog(jinja_env=app.jinja_env, root_url="/static/")
    catalog.add_folder(COMPONENTS_PATH)
    catalog.add_folder(TEMPLATES_PATH / template)
    catalog.add_folder(STATIC_PATH)
    app.wsgi_app = catalog.get_middleware(
        app.wsgi_app,
        autorefresh=auto_reload,
        allowed_ext=[".css", ".js", ".svg", ".woff", ".woff2"],
    )

    app.add_url_rule(
        "/",
        "index",
        lambda: catalog.render(
            "Resume",
            fileName=get_localized_file_name_without_extension(resume, translations),
            resume=resume,
        ),
    )

    return app
