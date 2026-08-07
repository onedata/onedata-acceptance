"""Tests for running a distributed demo-mode environment."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps import assert_distributed_rest_file_roundtrips
from tests.demo_mode.steps import (
    assert_onezone_configuration,
    run_oneprovider,
    run_onezone,
    run_second_oneprovider,
)

FIRST_FILE_CONTENT = b"Data stored through the first Oneprovider\n"
SECOND_FILE_CONTENT = b"Data stored through the second Oneprovider\n"


def test_distributed_environment(
    release: str,
    request: pytest.FixtureRequest,
) -> None:
    onezone_process = run_onezone(release, request)
    first_oneprovider_process = run_oneprovider(release, onezone_process, request)
    run_second_oneprovider(
        release,
        onezone_process,
        first_oneprovider_process,
        request,
    )
    assert_onezone_configuration(release)
    assert_distributed_rest_file_roundtrips(
        release,
        FIRST_FILE_CONTENT,
        SECOND_FILE_CONTENT,
    )
