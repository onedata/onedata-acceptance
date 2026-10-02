"""Steps for running the Python-access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.python_access import (
    build_python_access_command,
    prepare_python_access_directory,
    read_setup_log,
    run_python_access_command,
)


@log_step("Checking Python access example output")
def assert_python_access_example_output(
    command_output: str,
    expected_output: str,
) -> None:
    """Assert that the Python access example returned the expected output."""
    assert command_output == expected_output, (
        f"Expected Python access output {expected_output!r}, got {command_output!r}"
    )


@log_step("Running Python access example")
def run_python_access_example(
    request: pytest.FixtureRequest,
    timeout: float = 600,
) -> str:
    """Prepare and run the Python access example in its generated venv."""
    environment_root = prepare_python_access_directory(request)
    setup_log_path = environment_root / "setup.log"
    command = build_python_access_command(setup_log_path)
    try:
        return run_python_access_command(command, environment_root, timeout)
    except AssertionError as error:
        setup_log = read_setup_log(setup_log_path)
        raise AssertionError(
            f"Python access example failed:\nsetup output:\n{setup_log}\n{error}"
        ) from error
