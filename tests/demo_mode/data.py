"""Create and inspect data in a running demo-mode environment."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.constants import SPACE_APPEARANCE_TIMEOUT, SPACE_SYNC_TIMEOUT
from tests.demo_mode.environment import Oneprovider, Onezone
from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.rest import (
    OneproviderRestClient,
    OnezoneRestClient,
    get_oneprovider_configuration,
)
from tests.utils.docker_utils import container_ip
from tests.utils.http_exceptions import HTTPBadRequest, HTTPNotFound
from tests.utils.utils import repeat_failed


@log_step("Creating provider space")
def create_space_for_provider(
    onezone: Onezone,
    provider: Oneprovider,
    *,
    space_name: str,
    access_token: str,
) -> str:
    """Create a space supported by the selected Oneprovider."""
    onezone_client = _onezone_rest_client(onezone, access_token)
    provider_client = _oneprovider_rest_client(provider, access_token)

    space_id = onezone_client.create_space(name=space_name)
    support_token = onezone_client.create_space_support_token(space_id=space_id)
    storage_ids = provider_client.storage_ids()
    if not storage_ids:
        raise AssertionError("Demo Oneprovider has no storage available")
    provider_client.support_space(
        support_token=support_token,
        storage_id=storage_ids[0],
    )
    _await_accessible_space(provider_client, space_id)
    return space_id


@log_step("Getting REST space ID")
def get_space_id(
    provider: Oneprovider,
    *,
    space_name: str,
    access_token: str,
) -> str:
    """Get the ID of the named space accessible through a Oneprovider."""
    return _oneprovider_rest_client(provider, access_token).space_id(name=space_name)


@log_step("Uploading file")
def upload_file(
    provider: Oneprovider,
    *,
    space_id: str,
    file_name: str,
    content: bytes,
    access_token: str,
) -> None:
    """Upload a file through the selected Oneprovider."""
    _oneprovider_rest_client(provider, access_token).upload(
        space_id=space_id,
        file_name=file_name,
        content=content,
    )


def get_oneprovider_id(provider: Oneprovider) -> str:
    """Return the validated ID exposed by a Oneprovider."""
    configuration = get_oneprovider_configuration(container_ip(provider.container))
    provider_id = configuration.get("providerId")
    assert isinstance(provider_id, str), (
        f"Expected {provider.container} to expose a string provider ID, got {provider_id!r}"
    )
    assert provider_id, f"Expected {provider.container} to expose a non-empty provider ID"
    return provider_id


@log_step("Checking REST file content")
def assert_file_content(
    provider: Oneprovider,
    *,
    space_id: str,
    file_name: str,
    expected_content: bytes,
    access_token: str,
) -> None:
    _assert_file_content(
        provider,
        space_id=space_id,
        file_name=file_name,
        expected_content=expected_content,
        access_token=access_token,
    )


@log_step("Awaiting REST file content")
@repeat_failed(
    timeout=SPACE_SYNC_TIMEOUT,
    interval=1,
    exceptions=(AssertionError, HTTPBadRequest, HTTPNotFound),
)
def await_file_content(
    provider: Oneprovider,
    *,
    space_id: str,
    file_name: str,
    expected_content: bytes,
    access_token: str,
) -> None:
    _assert_file_content(
        provider,
        space_id=space_id,
        file_name=file_name,
        expected_content=expected_content,
        access_token=access_token,
    )


@log_step("Checking Oneprovider space support")
def assert_space_support(
    provider: Oneprovider,
    *,
    space_id: str,
    access_token: str,
) -> None:
    supported_space_ids = _oneprovider_rest_client(
        provider,
        access_token,
    ).supported_space_ids()

    assert space_id in supported_space_ids, (
        f"Expected space {space_id} to be supported by {provider.container}"
    )


def _onezone_rest_client(
    onezone: Onezone,
    access_token: str,
) -> OnezoneRestClient:
    return OnezoneRestClient(
        host=container_ip(onezone.container),
        access_token=access_token,
    )


def _oneprovider_rest_client(
    oneprovider: Oneprovider,
    access_token: str,
) -> OneproviderRestClient:
    return OneproviderRestClient(
        host=container_ip(oneprovider.container),
        access_token=access_token,
    )


def _assert_file_content(
    provider: Oneprovider,
    *,
    space_id: str,
    file_name: str,
    expected_content: bytes,
    access_token: str,
) -> None:
    downloaded_content = _oneprovider_rest_client(
        provider,
        access_token,
    ).download(
        space_id=space_id,
        file_name=file_name,
    )
    assert downloaded_content == expected_content, (
        f"{provider.container} returned {downloaded_content!r}, expected {expected_content!r}"
    )


@repeat_failed(
    timeout=SPACE_APPEARANCE_TIMEOUT,
    interval=1,
    exceptions=AssertionError,
)
def _await_accessible_space(
    provider_client: OneproviderRestClient,
    space_id: str,
) -> None:
    assert space_id in provider_client.accessible_space_ids(), (
        f"Space {space_id} has not appeared at {provider_client.host}"
    )
