"""Tests for the Python access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.constants import DEMO_SPACE_NAME
from tests.demo_mode.meta_steps.environment import start_foreground_environment
from tests.demo_mode.steps.python_access import (
    run_python_access_example,
)
from tests.demo_mode.utils.commands import DemoCommands


def test_python_access(demo_commands: DemoCommands, request: pytest.FixtureRequest) -> None:
    expected_output = f"['{DEMO_SPACE_NAME}']\nTEST\n"

    start_foreground_environment(demo_commands)

    command_output = run_python_access_example(demo_commands, request)
    assert command_output == expected_output, (
        f"Expected Python access output {expected_output!r}, got {command_output!r}"
    )
