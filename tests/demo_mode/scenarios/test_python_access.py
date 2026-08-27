"""Tests for the Python access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.constants import DEMO_SPACE_NAME
from tests.demo_mode.meta_steps.environment import start_foreground_environment
from tests.demo_mode.steps.examples import (
    assert_python_access_example_output,
    run_python_access_example,
)


def test_python_access(
    release: str,
    request: pytest.FixtureRequest,
) -> None:
    expected_output = f"['{DEMO_SPACE_NAME}']\nTEST\n"

    start_foreground_environment(release, request)

    command_output = run_python_access_example(request)
    assert_python_access_example_output(command_output, expected_output)
