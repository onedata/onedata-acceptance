"""Tests for running the demo-mode environment in the background."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.meta_steps import assert_rest_file_roundtrip
from tests.demo_mode.steps import (
    assert_onezone_configuration,
    run_oneprovider_in_background,
    run_onezone_in_background,
)

TEST_FILE_CONTENT = b"Onedata demo-mode background REST test\n"


def test_run_in_background(release: str) -> None:
    run_onezone_in_background(release)
    run_oneprovider_in_background(release)
    assert_onezone_configuration(release)
    assert_rest_file_roundtrip(release, TEST_FILE_CONTENT)
