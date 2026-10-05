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
    get_rest_space_id,
)
from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.rest import OneproviderRestClient, OnezoneRestClient


def test_run_in_background(
    release: str,
    demo_commands: DemoCommands,
    request: pytest.FixtureRequest,
) -> None:
    test_file_name = "background-rest-test.txt"
    test_file_content = b"Onedata demo-mode background REST test\n"

    environment = start_background_environment(demo_commands)
    access_token = environment.oneproviders[0].demo_access_token()
    onezone = OnezoneRestClient(environment.onezone, access_token)
    provider = OneproviderRestClient(environment.oneproviders[0], access_token)
    assert_onezone_configuration(onezone, release=release)

    space_id = get_rest_space_id(provider)
    upload_and_verify_rest_file_content(
        provider,
        space_id=space_id,
        file_name=test_file_name,
        content=test_file_content,
        request=request,
    )
