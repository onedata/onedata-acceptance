"""Tests for running a distributed demo-mode environment."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.environment import (
    assert_environment_configuration,
    start_foreground_environment,
)
from tests.demo_mode.steps.environment import get_demo_access_token
from tests.demo_mode.steps.rest import (
    assert_file_content,
    assert_space_support,
    create_space_for_provider,
    get_oneprovider_id,
    upload_rest_file,
)
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
    first_provider, second_provider = environment.oneproviders
    access_token = get_demo_access_token(first_provider, demo_commands)
    assert_environment_configuration(environment, demo_commands, release=release)

    first_provider_id = get_oneprovider_id(
        first_provider,
        access_token=access_token,
    )
    second_provider_id = get_oneprovider_id(
        second_provider,
        access_token=access_token,
    )
    assert first_provider_id != second_provider_id, (
        f"Distributed Oneproviders expose the same ID: {first_provider_id}"
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

    assert_space_support(
        second_provider,
        space_id=first_space_id,
        expected=False,
        access_token=access_token,
    )
    assert_space_support(
        first_provider,
        space_id=second_space_id,
        expected=False,
        access_token=access_token,
    )

    upload_rest_file(
        first_provider,
        space_id=first_space_id,
        file_name=first_file_name,
        content=first_file_content,
        access_token=access_token,
        request=request,
    )
    assert_file_content(
        first_provider,
        space_id=first_space_id,
        file_name=first_file_name,
        expected_content=first_file_content,
        access_token=access_token,
    )

    upload_rest_file(
        second_provider,
        space_id=second_space_id,
        file_name=second_file_name,
        content=second_file_content,
        access_token=access_token,
        request=request,
    )
    assert_file_content(
        second_provider,
        space_id=second_space_id,
        file_name=second_file_name,
        expected_content=second_file_content,
        access_token=access_token,
    )
