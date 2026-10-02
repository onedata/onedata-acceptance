"""Helpers for running the Python-access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial
from pathlib import Path
from shlex import quote
from shutil import rmtree

import pytest

from tests.demo_mode.utils.commands import Command, CommandTemplate


def prepare_python_access_directory(request: pytest.FixtureRequest) -> Path:
    """Create the temporary directory used by the Python-access example."""
    environment_root = Path("/tmp/demo-mode-python-access")
    if environment_root.exists():
        raise FileExistsError(f"Python access directory already exists: {environment_root}")
    environment_root.mkdir()
    request.addfinalizer(partial(rmtree, environment_root, ignore_errors=True))
    return environment_root


def build_python_access_command(setup_log_path: Path) -> str:
    """Build the shell command that sets up and runs the Python example."""
    setup_script = CommandTemplate("python_access/setup_environment.sh").path
    access_script = CommandTemplate("python_access/check_python_access.py").path
    quoted_setup_script = quote(str(setup_script))
    quoted_setup_log_path = quote(str(setup_log_path))
    quoted_access_script = quote(str(access_script))

    return "\n".join(
        (
            "set -e",
            f"source {quoted_setup_script} > {quoted_setup_log_path} 2>&1",
            f"python3 {quoted_access_script}",
        )
    )


def run_python_access_command(
    command: str,
    environment_root: Path,
    timeout: float,
) -> str:
    """Run the dynamically composed Python-access command."""
    return Command(
        text=command,
        name="python-access",
        cwd=environment_root,
    ).run(timeout=timeout)


def read_setup_log(setup_log_path: Path) -> str:
    """Read the Python-access setup log, returning a fallback when absent."""
    if not setup_log_path.exists():
        return "Setup log was not created"

    return setup_log_path.read_text(encoding="utf-8", errors="replace")
