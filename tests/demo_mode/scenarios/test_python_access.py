"""Tests for the Python access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.environment import run_onezone_with_oneprovider
from tests.demo_mode.meta_steps.examples import run_python_access_example
from tests.demo_mode.steps.examples import assert_python_access_example_output


def test_python_access(
    release: str,
    demo_space_name: str,
    first_oneprovider_container_name: str,
    request: pytest.FixtureRequest,
) -> None:
    expected_output = f"['{demo_space_name}']\nTEST\n"

    run_onezone_with_oneprovider(
        release,
        first_oneprovider_container_name,
        request,
    )

    command_output = run_python_access_example(request)
    assert_python_access_example_output(command_output, expected_output)
