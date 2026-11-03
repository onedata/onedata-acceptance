"""Tests for running the demo-mode environment in the foreground."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.constants import DEMO_SPACE_ID, DEMO_SPACE_NAME
from tests.demo_mode.meta_steps.environment import start_foreground_environment
from tests.demo_mode.steps.environment import get_demo_access_token
from tests.demo_mode.steps.rest import assert_file_content, get_space_id, upload_file


def test_run_in_foreground(
    request: pytest.FixtureRequest,
) -> None:
    file_name = "foreground-rest-test.txt"
    file_content = b"Onedata demo-mode foreground REST test\n"

    environment = start_foreground_environment()
    (provider,) = environment.oneproviders
    access_token = get_demo_access_token(environment.onezone)

    space_id = get_space_id(provider, space_name=DEMO_SPACE_NAME, access_token=access_token)
    assert space_id == DEMO_SPACE_ID, f"Demo space id should be {DEMO_SPACE_ID}, but is {space_id}"

    upload_file(
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
