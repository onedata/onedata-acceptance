"""Steps for running demo-mode examples."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial
from pathlib import Path
from shlex import quote
from shutil import rmtree
from tempfile import mkdtemp

import pytest

from tests.demo_mode.utils.commands import command_path, load_command, run_command
from tests.demo_mode.utils.logging import (
    log_running_command,
    log_step_done,
    log_step_start,
)


def run_comprehensive_example(release: str, timeout: float = 480) -> str:
    """Run the comprehensive example command and return its output."""
    description = "Running comprehensive example"
    log_step_start(description)

    command = load_command("comprehensive_example/example.sh", release)
    log_running_command(command)
    try:
        result = run_command(command, timeout=timeout, capture_output=True)
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"Comprehensive example did not finish within {timeout}s"
        ) from error
    assert result.returncode == 0, (
        "Comprehensive example failed with exit code "
        f"{result.returncode}:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    log_step_done(description)
    return result.stdout


def run_python_access_example(
    request: pytest.FixtureRequest,
    timeout: float = 480,
) -> str:
    """Prepare and run the Python access example in its generated venv."""
    description = "Running Python access example"
    log_step_start(description)

    environment_root = Path(mkdtemp(prefix="demo-mode-python-access-"))
    request.addfinalizer(partial(rmtree, environment_root, ignore_errors=True))

    setup_script = command_path("python_access/setup_environment.sh")
    access_script = command_path("python_access/check_python_access.py")
    python = environment_root / "venv" / "bin" / "python"
    setup_log_path = environment_root / "setup.log"
    command = "\n".join(
        (
            "set -e",
            f"source {quote(str(setup_script))} > {quote(str(setup_log_path))} 2>&1",
            f"{quote(str(python))} {quote(str(access_script))}",
        )
    )
    log_running_command(command)
    try:
        result = run_command(
            command,
            timeout=timeout,
            capture_output=True,
            cwd=environment_root,
        )
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"Python access example did not finish within {timeout}s"
        ) from error
    setup_log = (
        setup_log_path.read_text(encoding="utf-8", errors="replace")
        if setup_log_path.exists()
        else "Setup log was not created"
    )
    assert result.returncode == 0, (
        "Python access example failed with exit code "
        f"{result.returncode}:\nsetup output:\n{setup_log}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    log_step_done(description)
    return result.stdout


def get_comprehensive_example_file_name(command_output: str) -> str:
    """Extract the created filename from comprehensive-example output."""
    description = "Checking comprehensive example output"
    log_step_start(description)

    output_lines = [
        line
        for line in command_output.splitlines()
        if line.startswith("All done! Created a file called ")
    ]
    assert len(output_lines) == 1, (
        "Expected one comprehensive-example success message, got "
        f"{output_lines!r} in output:\n{command_output}"
    )
    message_parts = output_lines[0].split('"')
    assert (
        len(message_parts) >= 3
    ), f"Could not extract a filename from: {output_lines[0]!r}"
    file_name = message_parts[1]
    assert file_name.endswith(
        ".txt"
    ), f"Expected comprehensive example to create a .txt file, got {file_name!r}"

    log_step_done(description)
    return file_name


def assert_python_access_example_output(
    command_output: str,
    expected_output: str,
) -> None:
    """Assert that the Python access example returned the expected output."""
    description = "Checking Python access example output"
    log_step_start(description)

    assert (
        command_output == expected_output
    ), f"Expected Python access output {expected_output!r}, got {command_output!r}"

    log_step_done(description)
