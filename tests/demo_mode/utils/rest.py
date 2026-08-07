"""REST helpers for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from typing import Final, cast
from uuid import uuid4

from tests import OP_REST_PORT, OZ_REST_PORT, PANEL_REST_PORT
from tests.demo_mode.utils.common import (
    FIRST_ONEPROVIDER_CONTAINER_NAME,
    ONEZONE_CONTAINER_NAME,
)
from tests.type_definitions import JsonObject
from tests.utils.docker_utils import docker_ip
from tests.utils.rest_utils import (
    get_panel_rest_path,
    get_provider_rest_path,
    get_zone_rest_path,
    http_delete,
    http_get,
    http_post,
    http_put,
)
from tests.utils.utils import repeat_failed

TEST_SPACE_NAME: Final = "demo-mode-rest-space"
SPACE_SUPPORT_SIZE: Final = 1024**3
SPACE_APPEARANCE_TIMEOUT: Final = 60.0


def _authorization_headers(access_token: str) -> dict[str, str]:
    return {"X-Auth-Token": access_token}


def get_onezone_configuration() -> JsonObject:
    """Get the public configuration exposed by the demo Onezone REST API."""
    response = http_get(
        ip=docker_ip(ONEZONE_CONTAINER_NAME),
        port=OZ_REST_PORT,
        path=get_zone_rest_path("configuration"),
    )
    return cast(JsonObject, response.json())


def get_oneprovider_configuration(provider_container: str) -> JsonObject:
    """Get the public configuration exposed by a demo Oneprovider REST API."""
    response = http_get(
        ip=docker_ip(provider_container),
        port=OP_REST_PORT,
        path=get_provider_rest_path("configuration"),
    )
    return cast(JsonObject, response.json())


def _list_accessible_space_ids(
    provider_container: str,
    access_token: str,
) -> list[str]:
    response = http_get(
        ip=docker_ip(provider_container),
        port=OP_REST_PORT,
        path=get_provider_rest_path("spaces"),
        headers=_authorization_headers(access_token),
    )
    spaces = cast(list[JsonObject], response.json())
    return [cast(str, space["spaceId"]) for space in spaces]


def _list_user_space_ids(access_token: str) -> list[str]:
    response = http_get(
        ip=docker_ip(ONEZONE_CONTAINER_NAME),
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces"),
        headers=_authorization_headers(access_token),
    )
    response_body = cast(JsonObject, response.json())
    return cast(list[str], response_body["spaces"])


def _create_space(space_name: str, access_token: str) -> str:
    response = http_post(
        ip=docker_ip(ONEZONE_CONTAINER_NAME),
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces"),
        headers=_authorization_headers(access_token),
        data=json.dumps({"name": space_name}),
    )
    location = response.headers.get("Location")
    if not location:
        raise AssertionError("Onezone did not return the created space location")
    return location.rstrip("/").rsplit("/", maxsplit=1)[-1]


def _list_onepanel_resource_ids(
    provider_container: str,
    resource: str,
    access_token: str,
) -> list[str]:
    response = http_get(
        ip=docker_ip(provider_container),
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", resource),
        headers=_authorization_headers(access_token),
    )
    response_body = cast(JsonObject, response.json())
    return cast(list[str], response_body["ids"])


def _create_space_support_token(space_id: str, access_token: str) -> str:
    response = http_post(
        ip=docker_ip(ONEZONE_CONTAINER_NAME),
        port=OZ_REST_PORT,
        path=get_zone_rest_path("spaces", space_id, "providers", "token"),
        headers=_authorization_headers(access_token),
    )
    response_body = cast(JsonObject, response.json())
    return cast(str, response_body["token"])


def _get_first_storage_id(provider_container: str, access_token: str) -> str:
    storage_ids = _list_onepanel_resource_ids(
        provider_container,
        "storages",
        access_token,
    )
    if not storage_ids:
        raise AssertionError("Demo Oneprovider has no storage available")
    return storage_ids[0]


def _submit_space_support(
    provider_container: str,
    support_token: str,
    storage_id: str,
    access_token: str,
) -> None:
    http_post(
        ip=docker_ip(provider_container),
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "spaces"),
        headers=_authorization_headers(access_token),
        data=json.dumps(
            {
                "token": support_token,
                "size": SPACE_SUPPORT_SIZE,
                "storageId": storage_id,
            }
        ),
    )


def _support_space(
    provider_container: str,
    space_id: str,
    access_token: str,
) -> None:
    if space_id in get_provider_supported_space_ids(
        provider_container,
        access_token,
    ):
        return

    _submit_space_support(
        provider_container,
        _create_space_support_token(space_id, access_token),
        _get_first_storage_id(provider_container, access_token),
        access_token,
    )


def _get_or_create_user_space(access_token: str) -> str:
    user_space_ids = _list_user_space_ids(access_token)
    return (
        user_space_ids[0]
        if user_space_ids
        else _create_space(TEST_SPACE_NAME, access_token)
    )


@repeat_failed(
    timeout=SPACE_APPEARANCE_TIMEOUT,
    interval=1,
    exceptions=AssertionError,
)
def _wait_for_accessible_space(
    provider_container: str,
    space_id: str,
    access_token: str,
) -> str:
    assert space_id in _list_accessible_space_ids(
        provider_container, access_token
    ), f"Space {space_id} has not appeared in {provider_container}"
    return space_id


def get_provider_supported_space_ids(
    provider_container: str,
    access_token: str,
) -> list[str]:
    """Return the IDs of spaces supported locally by a Oneprovider."""
    return _list_onepanel_resource_ids(
        provider_container,
        "spaces",
        access_token,
    )


def create_and_support_space(
    provider_container: str,
    space_name: str,
    access_token: str,
) -> str:
    """Create a new user space and support it with the selected provider."""
    space_id = _create_space(space_name, access_token)
    _support_space(provider_container, space_id, access_token)
    return _wait_for_accessible_space(provider_container, space_id, access_token)


def get_or_create_supported_space(
    access_token: str,
    provider_container: str = FIRST_ONEPROVIDER_CONTAINER_NAME,
) -> str:
    """Return a supported space, creating and supporting one when needed."""
    supported_space_ids = get_provider_supported_space_ids(
        provider_container,
        access_token,
    )
    if supported_space_ids:
        return supported_space_ids[0]

    space_id = _get_or_create_user_space(access_token)
    _support_space(provider_container, space_id, access_token)
    return _wait_for_accessible_space(provider_container, space_id, access_token)


def _upload_file(
    provider_container: str,
    file_path: str,
    access_token: str,
    content: bytes,
) -> None:
    http_put(
        ip=docker_ip(provider_container),
        port=OP_REST_PORT,
        path=file_path,
        headers={
            **_authorization_headers(access_token),
            "Content-Type": "application/octet-stream",
        },
        data=content,
    )


def _download_file(
    provider_container: str,
    file_path: str,
    access_token: str,
) -> bytes:
    return http_get(
        ip=docker_ip(provider_container),
        port=OP_REST_PORT,
        path=file_path,
        headers=_authorization_headers(access_token),
    ).content


def _remove_file(
    provider_container: str,
    file_path: str,
    access_token: str,
) -> None:
    http_delete(
        ip=docker_ip(provider_container),
        port=OP_REST_PORT,
        path=file_path,
        headers=_authorization_headers(access_token),
    )


def download_and_remove_file(
    provider_container: str,
    access_token: str,
    space_id: str,
    file_name: str,
) -> bytes:
    """Download a file by path and remove it afterward."""
    file_path = get_provider_rest_path("data", space_id, "path", file_name)
    try:
        return _download_file(provider_container, file_path, access_token)
    finally:
        _remove_file(provider_container, file_path, access_token)


def upload_and_download_file(
    access_token: str,
    content: bytes,
    provider_container: str = FIRST_ONEPROVIDER_CONTAINER_NAME,
    space_id: str | None = None,
) -> bytes:
    """Upload a temporary text file through REST and download its content."""
    if space_id is None:
        space_id = get_or_create_supported_space(access_token, provider_container)
    file_name = f"demo-mode-rest-{uuid4().hex}.txt"
    file_path = get_provider_rest_path("data", space_id, "path", file_name)

    _upload_file(provider_container, file_path, access_token, content)
    try:
        return _download_file(provider_container, file_path, access_token)
    finally:
        _remove_file(provider_container, file_path, access_token)
