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
from tests.demo_mode.steps.environment import get_demo_access_token
from tests.demo_mode.steps.rest import create_space_for_provider
from tests.demo_mode.utils.commands import DemoCommands


def test_distributed_environment(
    release: str,
    demo_commands: DemoCommands,
    request: pytest.FixtureRequest,
) -> None:
    first_file_name = "first-provider-rest-test.txt"
    first_file_content = b"Data stored through the first Oneprovider\n"
    second_file_name = "second-provider-rest-test.txt"
    second_file_content = b"Data stored through the second Oneprovider\n"

    environment = start_foreground_environment(demo_commands, oneprovider_count=2)
    onezone = environment.onezone
    first_provider = environment.oneproviders[0]
    second_provider = environment.oneproviders[1]
    access_token = get_demo_access_token(first_provider, demo_commands)
    assert_onezone_configuration(onezone, release=release)

    assert_oneproviders_are_distinct(
        first_provider,
        second_provider,
        release=release,
        access_token=access_token,
    )

    first_space_id = create_space_for_provider(
        onezone,
        first_provider,
        space_name="demo-mode-first-provider-space",
        access_token=access_token,
    )
    second_space_id = create_space_for_provider(
        onezone,
        second_provider,
        space_name="demo-mode-second-provider-space",
        access_token=access_token,
    )
    assert_space_support_is_isolated(
        first_provider,
        second_provider,
        first_space_id=first_space_id,
        second_space_id=second_space_id,
        access_token=access_token,
    )

    upload_and_verify_rest_file_content(
        first_provider,
        space_id=first_space_id,
        file_name=first_file_name,
        content=first_file_content,
        access_token=access_token,
        request=request,
    )
    upload_and_verify_rest_file_content(
        second_provider,
        space_id=second_space_id,
        file_name=second_file_name,
        content=second_file_content,
        access_token=access_token,
        request=request,
    )
