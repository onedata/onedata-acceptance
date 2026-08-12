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


def test_python_access(
    release: str,
    demo_space_name: str,
    first_oneprovider_container_name: str,
    request: pytest.FixtureRequest,
) -> None:
    expected_output = f"['{demo_space_name}']\nTEST\n"

    onezone_process = run_onezone(release, request)
    run_oneprovider(
        release,
        onezone_process,
        first_oneprovider_container_name,
        request,
    )

    command_output = run_python_access_example(request)

    assert (
        command_output == expected_output
    ), f"Expected Python access output {expected_output!r}, got {command_output!r}"
