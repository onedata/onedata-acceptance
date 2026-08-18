"""Tests for running a distributed demo-mode environment."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.rest import (
    assert_oneproviders_are_distinct,
    assert_onezone_configuration,
    assert_space_support_is_isolated,
    upload_and_verify_rest_file_content,
)
from tests.demo_mode.steps.environment import (
    run_oneprovider,
    run_onezone,
    run_second_oneprovider,
)
from tests.demo_mode.steps.rest import (
    create_space_for_provider,
    get_demo_access_token,
)


def test_distributed_environment(
    release: str,
    onezone_name: str,
    first_oneprovider: str,
    second_oneprovider: str,
    request: pytest.FixtureRequest,
) -> None:
    first_file_name = "first-provider-rest-test.txt"
    first_file_content = b"Data stored through the first Oneprovider\n"
    second_file_name = "second-provider-rest-test.txt"
    second_file_content = b"Data stored through the second Oneprovider\n"

    onezone = run_onezone(release, request)
    run_oneprovider(release, onezone, first_oneprovider, request)
    run_second_oneprovider(release, onezone, second_oneprovider, request)
    assert_onezone_configuration(release, onezone_name)

    assert_oneproviders_are_distinct(first_oneprovider, second_oneprovider, release)

    access_token = get_demo_access_token(release)
    first_space_id = create_space_for_provider(
        first_oneprovider,
        "demo-mode-first-provider-space",
        access_token,
    )
    second_space_id = create_space_for_provider(
        second_oneprovider,
        "demo-mode-second-provider-space",
        access_token,
    )
    assert_space_support_is_isolated(
        first_oneprovider,
        first_space_id,
        second_oneprovider,
        second_space_id,
        access_token,
    )

    upload_and_verify_rest_file_content(
        first_oneprovider,
        first_space_id,
        first_file_name,
        access_token,
        first_file_content,
        request,
    )
    upload_and_verify_rest_file_content(
        second_oneprovider,
        second_space_id,
        second_file_name,
        access_token,
        second_file_content,
        request,
    )
