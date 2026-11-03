"""Helpers for running the Python-access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from pathlib import Path
from shlex import quote

from tests.demo_mode.utils.commands.command import Command
from tests.demo_mode.utils.commands.command_template import command_path

_SETUP_SCRIPT = command_path("python_access/setup_environment.sh")
_ACCESS_SCRIPT = command_path("python_access/check_python_access.py")


def run_python_access(
    *,
    environment_root: Path,
    setup_log_path: Path,
    timeout: float,
) -> str:
    """Build and run the Python-access guide fragments."""
    command = "\n".join(
        (
            "set -e",
            f"source {quote(str(_SETUP_SCRIPT))} > {quote(str(setup_log_path))} 2>&1",
            f"python3 {quote(str(_ACCESS_SCRIPT))}",
        )
    )
    return Command(command, "python-access", environment_root).run(timeout=timeout)


def read_setup_log(setup_log_path: Path) -> str:
    """Read the Python-access setup log, returning a fallback when absent."""
    if not setup_log_path.exists():
        return "Setup log was not created"

    return setup_log_path.read_text(encoding="utf-8", errors="replace")
