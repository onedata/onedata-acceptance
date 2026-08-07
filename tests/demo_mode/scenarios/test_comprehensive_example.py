"""Tests for the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.meta_steps import assert_comprehensive_example
from tests.demo_mode.steps import (
    assert_onezone_configuration,
    run_comprehensive_example,
)


def test_comprehensive_example(release: str) -> None:
    command_output = run_comprehensive_example(release)
    assert_onezone_configuration(release)
    assert_comprehensive_example(release, command_output)
