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


def test_distributed_environment(
    release: str,
    onezone_name: str,
    first_oneprovider_container_name: str,
    second_oneprovider_container_name: str,
    request: pytest.FixtureRequest,
) -> None:
    onezone_process = run_onezone(release, request)
    first_oneprovider_process = run_oneprovider(release, onezone_process, request)
    run_second_oneprovider(
        release,
        onezone_process,
        first_oneprovider_process,
        second_oneprovider_container_name,
        request,
    )
    assert_onezone_configuration(release, onezone_name)
    assert_distributed_rest_file_roundtrips(
        release,
        b"Data stored through the first Oneprovider\n",
        b"Data stored through the second Oneprovider\n",
        first_oneprovider_container_name,
        second_oneprovider_container_name,
    )
