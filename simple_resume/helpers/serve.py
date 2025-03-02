"""Contains helpers to serve a JSON Resume."""

from __future__ import annotations

import errno
from threading import Thread
from typing import TYPE_CHECKING

from flask import Flask
from jinjax import Catalog
from livereload import Server

from simple_resume.helpers.constants import (
    COMPONENTS_PATH,
    STATIC_PATH,
    TEMPLATES_PATH,
    UI_HELPERS_PATH,
)
from simple_resume.helpers.i18n import get_localized_file_name_without_extension, get_translations
from simple_resume.helpers.jinja import (
    add_custom_filters_to_jinja_environment,
    add_i18n_support_to_jinja_environment,
)

if TYPE_CHECKING:
    from simple_resume.models.json_resume import JsonResume


def serve_resume_for_development(resume: JsonResume, port: int) -> None:
    """Serve a JSON Resume with live reloading.

    Args:
        resume: A validated JSON Resume.
        port: The port on which the server should listen.
    """
    app = _create_flask_app_for_resume(resume)
    app.debug = True

    server = Server(app.wsgi_app)
    server.watch("**/*.jinja")
    server.watch("**/*.css")
    server.watch("**/*.js")

    try:
        server.serve(port=port)
    except OSError as error:
        if error.errno == errno.EADDRINUSE:
            error_message = f"Port {port} is already in use, please choose another port."
            raise ValueError(error_message) from None
        raise


def serve_resume_for_export(resume: JsonResume, port: int) -> None:
    """Serve a JSON Resume without live reloading.

    Args:
        resume: A validated JSON Resume.
        port: The port on which the server should listen.
    """
    app = _create_flask_app_for_resume(resume)

    thread = Thread(target=app.run, daemon=True, kwargs={"port": port})
    thread.start()


def _create_flask_app_for_resume(resume: JsonResume) -> Flask:
    """Create a Flask application to serve a JSON Resume.

    Args:
        resume: A validated JSON Resume.

    Returns:
        A Flask application instance configured to serve the JSON Resume.
    """
    app = Flask(__name__)

    simple_resume_metadata = resume.meta.simple_resume
    language = simple_resume_metadata.language
    translations = get_translations(language)

    add_i18n_support_to_jinja_environment(app.jinja_env, translations)
    add_custom_filters_to_jinja_environment(app.jinja_env, language, translations)

    # Auto-reload is disabled because it is handled by the livereload server.
    auto_reload = False
    app.jinja_env.auto_reload = auto_reload
    app.config["TEMPLATES_AUTO_RELOAD"] = auto_reload

    catalog = Catalog(jinja_env=app.jinja_env, root_url="/static/")
    catalog.add_folder(COMPONENTS_PATH)
    catalog.add_folder(TEMPLATES_PATH / simple_resume_metadata.template.name)
    catalog.add_folder(STATIC_PATH)
    catalog.add_folder(UI_HELPERS_PATH)
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
