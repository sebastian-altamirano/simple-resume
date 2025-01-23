"""Contains the main logic of the CLI application."""

from __future__ import annotations

from typer import Typer

from simple_resume import commands

app = Typer()

app.command()(commands.export)
app.command()(commands.serve)
app.command()(commands.validate)
