"""Tests for the Python access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from pathlib import Path

from tests.demo_mode.constants import DEMO_SPACE_NAME
from tests.demo_mode.environment import start_foreground_environment
from tests.demo_mode.python_access import assert_python_access_example_output


def test_python_access(tmp_path: Path) -> None:
    expected_output = f"['{DEMO_SPACE_NAME}']\nTEST\n"

    start_foreground_environment()
    assert_python_access_example_output(
        expected_output=expected_output,
        environment_root=tmp_path,
    )
