"""Tests for running a distributed demo-mode environment."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.environment import start_foreground_environment
from tests.demo_mode.meta_steps.rest import (
    assert_oneproviders_are_distinct,
    assert_onezone_configuration,
    assert_space_support_is_isolated,
    upload_and_verify_rest_file_content,
)
from tests.demo_mode.steps.rest import (
    create_space_for_provider,
    get_demo_access_token,
)


def test_distributed_environment(
    release: str,
    onezone_name: str,
    onezone_container: str,
    first_oneprovider_container: str,
    second_oneprovider_container: str,
    request: pytest.FixtureRequest,
) -> None:
    first_file_name = "first-provider-rest-test.txt"
    first_file_content = b"Data stored through the first Oneprovider\n"
    second_file_name = "second-provider-rest-test.txt"
    second_file_content = b"Data stored through the second Oneprovider\n"

    start_foreground_environment(
        release,
        onezone_container,
        first_oneprovider_container,
        request,
        second_oneprovider_container,
    )
    assert_onezone_configuration(release, onezone_name)

    assert_oneproviders_are_distinct(
        first_oneprovider_container,
        second_oneprovider_container,
        release,
    )

    access_token = get_demo_access_token(release)
    first_space_id = create_space_for_provider(
        first_oneprovider_container,
        "demo-mode-first-provider-space",
        access_token,
    )
    second_space_id = create_space_for_provider(
        second_oneprovider_container,
        "demo-mode-second-provider-space",
        access_token,
    )
    assert_space_support_is_isolated(
        first_oneprovider_container,
        first_space_id,
        second_oneprovider_container,
        second_space_id,
        access_token,
    )

    upload_and_verify_rest_file_content(
        first_oneprovider_container,
        first_space_id,
        first_file_name,
        access_token,
        first_file_content,
        request,
    )
    upload_and_verify_rest_file_content(
        second_oneprovider_container,
        second_space_id,
        second_file_name,
        access_token,
        second_file_content,
        request,
    )
