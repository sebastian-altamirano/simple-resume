#!/usr/bin/python3

"""The entry point of the CLI application."""

from __future__ import annotations

import asyncio
from multiprocessing import freeze_support
from sys import platform

from simple_resume.main import app

if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

freeze_support()

app(prog_name="simple-resume")
