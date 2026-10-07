"""Steps for demo-mode REST operations."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

import pytest

from tests.demo_mode.constants import DEMO_SPACE_NAME
from tests.demo_mode.type_definitions import Oneprovider, Onezone
from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.rest import OneproviderRestClient, OnezoneRestClient
from tests.utils.docker_utils import container_ip


def onezone_rest_client(
    onezone: Onezone,
    access_token: str | None = None,
) -> OnezoneRestClient:
    return OnezoneRestClient(
        host=container_ip(onezone.container),
        access_token=access_token,
    )


def oneprovider_rest_client(
    oneprovider: Oneprovider,
    access_token: str,
) -> OneproviderRestClient:
    return OneproviderRestClient(
        host=container_ip(oneprovider.container),
        access_token=access_token,
    )


@log_step("Creating provider space")
def create_space_for_provider(
    onezone: Onezone,
    provider: Oneprovider,
    *,
    space_name: str,
    access_token: str,
) -> str:
    """Create a space supported by the selected Oneprovider."""
    return oneprovider_rest_client(provider, access_token).create_and_support_space(
        onezone_rest_client(onezone, access_token),
        name=space_name,
    )


@log_step("Getting REST space ID")
def get_rest_space_id(
    provider: Oneprovider,
    *,
    access_token: str,
) -> str:
    """Get the ID of the demo space accessible through a Oneprovider."""
    return oneprovider_rest_client(provider, access_token).space_id(name=DEMO_SPACE_NAME)


def get_supported_space_ids(
    provider: Oneprovider,
    *,
    access_token: str,
) -> list[str]:
    """Return IDs of spaces supported by the selected Oneprovider."""
    return oneprovider_rest_client(provider, access_token).supported_space_ids()


@log_step("Removing REST file")
def remove_rest_file(
    provider: Oneprovider,
    *,
    space_id: str,
    file_name: str,
    access_token: str,
) -> None:
    """Remove a file through the selected Oneprovider."""
    oneprovider_rest_client(provider, access_token).remove(
        space_id=space_id,
        file_name=file_name,
    )


@log_step("Uploading REST file")
def upload_rest_file(
    provider: Oneprovider,
    *,
    space_id: str,
    file_name: str,
    content: bytes,
    access_token: str,
    request: pytest.FixtureRequest,
) -> None:
    """Upload a REST file and schedule its removal after the test."""
    oneprovider_rest_client(provider, access_token).upload(
        space_id=space_id,
        file_name=file_name,
        content=content,
    )
    request.addfinalizer(
        partial(
            remove_rest_file,
            provider,
            space_id=space_id,
            file_name=file_name,
            access_token=access_token,
        )
    )


@log_step("Downloading REST file")
def download_rest_file(
    provider: Oneprovider,
    *,
    space_id: str,
    file_name: str,
    access_token: str,
) -> bytes:
    """Download an existing file through REST."""
    return oneprovider_rest_client(provider, access_token).download(
        space_id=space_id,
        file_name=file_name,
    )
