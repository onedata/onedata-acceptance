"""Tests for running the demo-mode environment in the foreground."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.environment import (
    assert_environment_configuration,
    start_foreground_environment,
)
from tests.demo_mode.steps.environment import get_demo_access_token
from tests.demo_mode.steps.rest import assert_file_content, get_demo_space_id, upload_rest_file
from tests.demo_mode.utils.commands import DemoCommands


def test_run_in_foreground(
    release: str,
    demo_commands: DemoCommands,
    request: pytest.FixtureRequest,
) -> None:
    file_name = "foreground-rest-test.txt"
    file_content = b"Onedata demo-mode foreground REST test\n"

    environment = start_foreground_environment(demo_commands)
    (provider,) = environment.oneproviders
    access_token = get_demo_access_token(provider, demo_commands)
    assert_environment_configuration(environment, demo_commands, release=release)

    space_id = get_demo_space_id(provider, access_token=access_token)

    upload_rest_file(
        provider,
        space_id=space_id,
        file_name=file_name,
        content=file_content,
        access_token=access_token,
        request=request,
    )
    assert_file_content(
        provider,
        space_id=space_id,
        file_name=file_name,
        expected_content=file_content,
        access_token=access_token,
    )
