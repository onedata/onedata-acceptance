"""Tests for running a distributed demo-mode environment."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps import run_onezone_with_two_oneproviders
from tests.demo_mode.steps import (
    assert_oneproviders_are_distinct,
    assert_onezone_configuration,
    assert_rest_file_content,
    assert_space_support_is_isolated,
    create_space_for_provider,
    get_demo_access_token,
    upload_rest_file,
)


def test_distributed_environment(
    release: str,
    onezone_name: str,
    first_oneprovider_container_name: str,
    second_oneprovider_container_name: str,
    request: pytest.FixtureRequest,
) -> None:
    first_file_content = b"Data stored through the first Oneprovider\n"
    second_file_content = b"Data stored through the second Oneprovider\n"

    run_onezone_with_two_oneproviders(
        release,
        first_oneprovider_container_name,
        second_oneprovider_container_name,
        request,
    )
    assert_onezone_configuration(release, onezone_name)

    assert_oneproviders_are_distinct(
        first_oneprovider_container_name,
        second_oneprovider_container_name,
        release,
    )

    access_token = get_demo_access_token(release)
    first_space_id = create_space_for_provider(
        first_oneprovider_container_name,
        "demo-mode-first-provider-space",
        access_token,
    )
    second_space_id = create_space_for_provider(
        second_oneprovider_container_name,
        "demo-mode-second-provider-space",
        access_token,
    )
    assert_space_support_is_isolated(
        first_oneprovider_container_name,
        first_space_id,
        second_oneprovider_container_name,
        second_space_id,
        access_token,
    )

    first_file_name = upload_rest_file(
        first_oneprovider_container_name,
        first_space_id,
        access_token,
        first_file_content,
        request,
    )
    assert_rest_file_content(
        first_oneprovider_container_name,
        access_token,
        first_space_id,
        first_file_name,
        first_file_content,
    )
    second_file_name = upload_rest_file(
        second_oneprovider_container_name,
        second_space_id,
        access_token,
        second_file_content,
        request,
    )
    assert_rest_file_content(
        second_oneprovider_container_name,
        access_token,
        second_space_id,
        second_file_name,
        second_file_content,
    )
