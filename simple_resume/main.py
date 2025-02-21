"""Contains the main logic of the CLI application."""

from __future__ import annotations

from typer import Typer

from simple_resume import commands

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]}, pretty_exceptions_show_locals=False
)

app.command()(commands.export)
app.command()(commands.serve)
app.command()(commands.validate)
app.command()(commands.version)
