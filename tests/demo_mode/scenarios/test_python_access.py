"""Tests for the Python access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.steps.environment import run_oneprovider, run_onezone
from tests.demo_mode.steps.examples import (
    assert_python_access_example_output,
    run_python_access_example,
)


def test_python_access(
    release: str,
    demo_space_name: str,
    onezone_container: str,
    first_oneprovider: str,
    request: pytest.FixtureRequest,
) -> None:
    expected_output = f"['{demo_space_name}']\nTEST\n"

    onezone = run_onezone(release, onezone_container, request)
    run_oneprovider(release, onezone, first_oneprovider, request)

    command_output = run_python_access_example(request)
    assert_python_access_example_output(command_output, expected_output)
