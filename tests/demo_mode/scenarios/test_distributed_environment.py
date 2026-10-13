"""Tests for running a distributed demo-mode environment."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.constants import DEMO_SPACE_ID, DEMO_SPACE_NAME
from tests.demo_mode.meta_steps.environment import start_foreground_environment
from tests.demo_mode.steps.environment import get_demo_access_token
from tests.demo_mode.steps.rest import (
    assert_file_content,
    assert_space_support,
    await_file_content,
    get_oneprovider_id,
    get_space_id,
    upload_rest_file,
)


def test_distributed_environment(
    request: pytest.FixtureRequest,
) -> None:
    local_content = b"Data stored through the local Oneprovider\n"
    shared_content = b"Data written through op_test1, read through op_test2\n"

    environment = start_foreground_environment(
        oneprovider_count=2,
    )
    first, second = environment.oneproviders

    access_token = get_demo_access_token(environment.onezone)

    for provider in environment.oneproviders:
        assert_space_support(
            provider,
            space_id=DEMO_SPACE_ID,
            expected=True,
            access_token=access_token,
        )

        space_id = get_space_id(
            provider,
            space_name=DEMO_SPACE_NAME,
            access_token=access_token,
        )
        assert space_id == DEMO_SPACE_ID, (
            f"{provider.container} exposes demo-space as {space_id}, expected {DEMO_SPACE_ID}"
        )

        file_name = f"{provider.container}-local.txt"
        upload_rest_file(
            provider,
            space_id=DEMO_SPACE_ID,
            file_name=file_name,
            content=local_content,
            access_token=access_token,
            request=request,
        )
        assert_file_content(
            provider,
            space_id=DEMO_SPACE_ID,
            file_name=file_name,
            expected_content=local_content,
            access_token=access_token,
        )

    provider_ids = [get_oneprovider_id(provider) for provider in environment.oneproviders]
    assert len(set(provider_ids)) == len(provider_ids), provider_ids

    upload_rest_file(
        first,
        space_id=DEMO_SPACE_ID,
        file_name="shared.txt",
        content=shared_content,
        access_token=access_token,
        request=request,
    )
    await_file_content(
        second,
        space_id=DEMO_SPACE_ID,
        file_name="shared.txt",
        expected_content=shared_content,
        access_token=access_token,
    )
