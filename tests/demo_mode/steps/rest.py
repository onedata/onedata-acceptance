"""Steps for demo-mode REST operations."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

import pytest

from tests.demo_mode.constants import DEMO_SPACE_NAME
from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.rest import OneproviderRestClient, OnezoneRestClient


@log_step("Getting demo access token")
def get_demo_access_token(commands: DemoCommands) -> str:
    """Get the access token exposed by the demo environment."""
    access_token = commands.oneprovider_access_token().run().strip()
    if not access_token:
        raise AssertionError("The access-token command returned an empty result")
    return access_token


@log_step("Creating provider space")
def create_space_for_provider(
    onezone: OnezoneRestClient,
    provider: OneproviderRestClient,
    *,
    space_name: str,
) -> str:
    """Create a space supported by the selected Oneprovider."""
    return provider.create_and_support_space(onezone, name=space_name)


@log_step("Getting REST space ID")
def get_rest_space_id(provider: OneproviderRestClient) -> str:
    """Get the ID of the demo space accessible through a Oneprovider."""
    return provider.space_id(name=DEMO_SPACE_NAME)


@log_step("Uploading REST file")
def upload_rest_file(
    provider: OneproviderRestClient,
    *,
    space_id: str,
    file_name: str,
    content: bytes,
    request: pytest.FixtureRequest,
) -> None:
    """Upload a REST file and schedule its removal after the test."""
    provider.upload(
        space_id=space_id,
        file_name=file_name,
        content=content,
    )
    request.addfinalizer(
        partial(
            provider.remove,
            space_id=space_id,
            file_name=file_name,
        )
    )


@log_step("Downloading REST file")
def download_rest_file(
    provider: OneproviderRestClient,
    *,
    space_id: str,
    file_name: str,
) -> bytes:
    """Download an existing file through REST."""
    return provider.download(space_id=space_id, file_name=file_name)
