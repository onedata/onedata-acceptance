"""Tests for running the demo-mode environment in the background."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.environment import start_background_environment
from tests.demo_mode.meta_steps.rest import (
    assert_onezone_configuration,
    upload_and_verify_rest_file_content,
)
from tests.demo_mode.steps.rest import (
    get_demo_access_token,
    get_rest_space_id,
)


def test_run_in_background(
    release: str,
    onezone_name: str,
    demo_space_name: str,
    onezone_container: str,
    first_oneprovider_container: str,
    request: pytest.FixtureRequest,
) -> None:
    test_file_name = "background-rest-test.txt"
    test_file_content = b"Onedata demo-mode background REST test\n"

    start_background_environment(
        release,
        onezone_container,
        first_oneprovider_container,
        request,
    )
    assert_onezone_configuration(release, onezone_name)

    access_token = get_demo_access_token(release)
    space_id = get_rest_space_id(
        first_oneprovider_container,
        demo_space_name,
        access_token,
    )
    upload_and_verify_rest_file_content(
        first_oneprovider_container,
        space_id,
        test_file_name,
        access_token,
        test_file_content,
        request,
    )
