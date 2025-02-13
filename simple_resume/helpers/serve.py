"""Contains helpers to serve a JSON Resume."""

from __future__ import annotations

from threading import Thread
from typing import TYPE_CHECKING

from flask import Flask
from jinjax import Catalog
from livereload import Server

from simple_resume.helpers.constants import (
    COMPONENTS_PATH,
    STATIC_PATH,
    TEMPLATES_PATH,
)
from simple_resume.helpers.i18n import get_localized_file_name_without_extension
from simple_resume.helpers.jinja import (
    add_custom_filters_to_jinja_environment,
    add_i18n_support_to_jinja_environment,
)

if TYPE_CHECKING:
    from babel.support import NullTranslations

    from simple_resume.models.json_resume import JsonResume


def serve_resume_for_development(
    resume: JsonResume, template: str, language: str, port: int, translations: NullTranslations
) -> None:
    """Serve a JSON Resume with live reloading.

    Args:
        resume: The content of a JSON Resume file.
        template: The name of the template to use.
        language: The language tag of the language to use.
        port: The port on which the server should listen.
        translations: The message catalog to use.
    """
    app = _create_flask_app_for_resume(resume, template, language, translations)
    app.debug = True

    server = Server(app.wsgi_app)
    server.watch("**/*.jinja")
    server.watch("**/*.css")
    server.watch("**/*.js")

    server.serve(port=port)


def serve_resume_for_export(
    resume: JsonResume, template: str, language: str, port: int, translations: NullTranslations
) -> None:
    """Serve a JSON Resume without live reloading.

    Args:
        resume: The content of a JSON Resume file.
        template: The name of the template to use.
        language: The language tag of the language to use.
        port: The port on which the server should listen.
        translations: The message catalog to use.
    """
    app = _create_flask_app_for_resume(resume, template, language, translations)

    thread = Thread(target=app.run, daemon=True, kwargs={"port": port})
    thread.start()


def _create_flask_app_for_resume(
    resume: JsonResume, template: str, language: str, translations: NullTranslations
) -> Flask:
    """Create a Flask application to serve a JSON Resume.

    Args:
        resume: The content of a JSON Resume file.
        template: The name of the template to use.
        language: The language tag of the language to use.
        translations: The message catalog to use.

    Returns:
        A Flask application instance configured to serve the JSON Resume.
    """
    app = Flask(__name__)

    add_i18n_support_to_jinja_environment(app.jinja_env, translations)
    add_custom_filters_to_jinja_environment(app.jinja_env, language, translations)

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
            file_name=get_localized_file_name_without_extension(resume, translations),
            resume=resume,
        ),
    )

    return app
