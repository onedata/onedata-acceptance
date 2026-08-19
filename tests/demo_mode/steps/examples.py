"""Steps for running demo-mode examples."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess

import pytest

from tests.demo_mode.utils.commands import load_command, run_command
from tests.demo_mode.utils.examples import (
    build_python_access_command,
    prepare_python_access_directory,
    read_setup_log,
    run_python_access_command,
)
from tests.demo_mode.utils.logging import log_running_command, log_step


@log_step("Running comprehensive example")
def run_comprehensive_example(release: str, timeout: float = 480) -> str:
    """Run the comprehensive example command and return its output."""
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

    return result.stdout


@log_step("Checking comprehensive example success message")
def assert_comprehensive_example_success_message_count(
    output_lines: list[str],
    command_output: str,
) -> None:
    """Assert that comprehensive-example output has one success message."""
    assert len(output_lines) == 1, (
        "Expected one comprehensive-example success message, got "
        f"{output_lines!r} in output:\n{command_output}"
    )


@log_step("Checking comprehensive example filename message")
def assert_comprehensive_example_message_contains_file_name(
    message: str,
    message_parts: list[str],
) -> None:
    """Assert that a comprehensive-example message contains a filename."""
    assert len(message_parts) >= 3, f"Could not extract a filename from: {message!r}"


@log_step("Checking comprehensive example filename")
def assert_comprehensive_example_file_name(file_name: str) -> None:
    """Assert that the comprehensive example created a text file."""
    assert file_name.endswith(
        ".txt"
    ), f"Expected comprehensive example to create a .txt file, got {file_name!r}"


@log_step("Checking Python access example output")
def assert_python_access_example_output(
    command_output: str,
    expected_output: str,
) -> None:
    """Assert that the Python access example returned the expected output."""
    assert (
        command_output == expected_output
    ), f"Expected Python access output {expected_output!r}, got {command_output!r}"


@log_step("Running Python access example")
def run_python_access_example(
    request: pytest.FixtureRequest,
    timeout: float = 480,
) -> str:
    """Prepare and run the Python access example in its generated venv."""
    environment_root = prepare_python_access_directory(request)
    setup_log_path = environment_root / "setup.log"
    command = build_python_access_command(setup_log_path)
    result = run_python_access_command(command, environment_root, timeout)
    setup_log = read_setup_log(setup_log_path)

    assert result.returncode == 0, (
        "Python access example failed with exit code "
        f"{result.returncode}:\nsetup output:\n{setup_log}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    return result.stdout
