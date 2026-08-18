"""Tests for running the demo-mode environment in the foreground."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.rest import (
    assert_onezone_configuration,
    upload_and_verify_rest_file_content,
)
from tests.demo_mode.steps.environment import run_oneprovider, run_onezone
from tests.demo_mode.steps.rest import (
    get_demo_access_token,
    get_rest_space_id,
)


def test_run_in_foreground(
    release: str,
    onezone_name: str,
    demo_space_name: str,
    first_oneprovider: str,
    request: pytest.FixtureRequest,
) -> None:
    test_file_name = "foreground-rest-test.txt"
    test_file_content = b"Onedata demo-mode foreground REST test\n"

    onezone = run_onezone(release, request)
    run_oneprovider(release, onezone, first_oneprovider, request)

    assert_onezone_configuration(release, onezone_name)

    access_token = get_demo_access_token(release)
    space_id = get_rest_space_id(first_oneprovider, demo_space_name, access_token)
    upload_and_verify_rest_file_content(
        first_oneprovider,
        space_id,
        test_file_name,
        access_token,
        test_file_content,
        request,
    )
