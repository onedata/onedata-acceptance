"""Tests for running the demo-mode environment in the background."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.constants import DEMO_SPACE_ID, DEMO_SPACE_NAME
from tests.demo_mode.meta_steps.environment import (
    assert_environment_configuration,
    start_background_environment,
)
from tests.demo_mode.steps.environment import get_demo_access_token
from tests.demo_mode.steps.rest import assert_file_content, get_space_id, upload_rest_file
from tests.demo_mode.utils.commands import DemoCommands


def test_run_in_background(
    release: str,
    demo_commands: DemoCommands,
    request: pytest.FixtureRequest,
) -> None:
    file_name = "background-rest-test.txt"
    file_content = b"Onedata demo-mode background REST test\n"

    environment = start_background_environment(demo_commands)
    (provider,) = environment.oneproviders
    access_token = get_demo_access_token(provider, demo_commands)
    assert_environment_configuration(
        environment,
        release=release,
        access_token=access_token,
    )

    space_id = get_space_id(provider, space_name=DEMO_SPACE_NAME, access_token=access_token)
    assert space_id == DEMO_SPACE_ID, f"Demo space id should be {DEMO_SPACE_ID}, but is {space_id}"

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
