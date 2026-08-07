"""Tests for running the demo-mode environment in the foreground."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.steps import (
    assert_onezone_configuration,
    run_oneprovider,
    run_onezone,
)


def test_run_in_foreground(release: str, request: pytest.FixtureRequest) -> None:
    onezone_process = run_onezone(release, request)
    run_oneprovider(release, onezone_process, request)
    assert_onezone_configuration()
