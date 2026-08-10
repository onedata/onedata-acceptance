"""Tests for the Python access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.steps import (
    run_oneprovider,
    run_onezone,
    run_python_access_example,
)

EXPECTED_OUTPUT = "['demo-space']\nTEST\n"


def test_python_access(release: str, request: pytest.FixtureRequest) -> None:
    onezone_process = run_onezone(release, request)
    run_oneprovider(release, onezone_process, request)

    command_output = run_python_access_example(request)

    assert (
        command_output == EXPECTED_OUTPUT
    ), f"Expected Python access output {EXPECTED_OUTPUT!r}, got {command_output!r}"
