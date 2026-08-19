"""Composite steps for running demo-mode examples."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial
from pathlib import Path
from shlex import quote
from shutil import rmtree

import pytest

from tests.demo_mode.utils.commands import command_path, run_command
from tests.demo_mode.utils.logging import log_running_command, log_step


def _prepare_python_access_directory(
    request: pytest.FixtureRequest,
) -> Path:
    environment_root = Path("/tmp/demo-mode-python-access")
    if environment_root.exists():
        raise FileExistsError(
            f"Python access directory already exists: {environment_root}"
        )
    environment_root.mkdir()
    request.addfinalizer(partial(rmtree, environment_root, ignore_errors=True))
    return environment_root


def _build_python_access_command(setup_log_path: Path) -> str:
    setup_script = command_path("python_access/setup_environment.sh")
    access_script = command_path("python_access/check_python_access.py")
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


def _run_python_access_command(
    command: str,
    environment_root: Path,
    timeout: float,
) -> subprocess.CompletedProcess[str]:
    log_running_command(command)
    try:
        return run_command(
            command,
            timeout=timeout,
            capture_output=True,
            cwd=environment_root,
        )
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"Python access example did not finish within {timeout}s"
        ) from error


def _read_setup_log(setup_log_path: Path) -> str:
    if not setup_log_path.exists():
        return "Setup log was not created"

    return setup_log_path.read_text(encoding="utf-8", errors="replace")


@log_step("Running Python access example")
def run_python_access_example(
    request: pytest.FixtureRequest,
    timeout: float = 480,
) -> str:
    """Prepare and run the Python access example in its generated venv."""
    environment_root = _prepare_python_access_directory(request)
    setup_log_path = environment_root / "setup.log"
    command = _build_python_access_command(setup_log_path)
    result = _run_python_access_command(command, environment_root, timeout)
    setup_log = _read_setup_log(setup_log_path)

    assert result.returncode == 0, (
        "Python access example failed with exit code "
        f"{result.returncode}:\nsetup output:\n{setup_log}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    return result.stdout
