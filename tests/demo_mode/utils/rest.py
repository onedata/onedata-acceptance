"""REST helpers for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from time import monotonic, sleep
from typing import Final, cast
from uuid import uuid4

from tests import OP_REST_PORT, OZ_REST_PORT, PANEL_REST_PORT
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

ONEZONE_CONTAINER_NAME: Final = "oz_test"
ONEPROVIDER_CONTAINER_NAME: Final = "op_test1"
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


def _list_supported_space_ids(access_token: str) -> list[str]:
    response = http_get(
        ip=docker_ip(ONEPROVIDER_CONTAINER_NAME),
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


def _create_space(access_token: str) -> str:
    response = http_post(
        ip=docker_ip(ONEZONE_CONTAINER_NAME),
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces"),
        headers=_authorization_headers(access_token),
        data=json.dumps({"name": TEST_SPACE_NAME}),
    )
    location = response.headers.get("Location")
    if not location:
        raise AssertionError("Onezone did not return the created space location")
    return location.rstrip("/").rsplit("/", maxsplit=1)[-1]


def _list_onepanel_resource_ids(resource: str, access_token: str) -> list[str]:
    response = http_get(
        ip=docker_ip(ONEPROVIDER_CONTAINER_NAME),
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


def _get_first_storage_id(access_token: str) -> str:
    storage_ids = _list_onepanel_resource_ids("storages", access_token)
    if not storage_ids:
        raise AssertionError("Demo Oneprovider has no storage available")
    return storage_ids[0]


def _submit_space_support(
    support_token: str,
    storage_id: str,
    access_token: str,
) -> None:
    http_post(
        ip=docker_ip(ONEPROVIDER_CONTAINER_NAME),
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


def _support_space(space_id: str, access_token: str) -> None:
    if space_id in _list_onepanel_resource_ids("spaces", access_token):
        return

    _submit_space_support(
        _create_space_support_token(space_id, access_token),
        _get_first_storage_id(access_token),
        access_token,
    )


def _get_or_create_user_space(access_token: str) -> str:
    user_space_ids = _list_user_space_ids(access_token)
    return user_space_ids[0] if user_space_ids else _create_space(access_token)


def _wait_for_supported_space(space_id: str, access_token: str) -> str:
    deadline = monotonic() + SPACE_APPEARANCE_TIMEOUT
    while monotonic() < deadline:
        if space_id in _list_supported_space_ids(access_token):
            return space_id
        sleep(1)

    raise AssertionError(
        f"Space {space_id} did not appear in Oneprovider within "
        f"{SPACE_APPEARANCE_TIMEOUT:g}s"
    )


def get_or_create_supported_space(access_token: str) -> str:
    """Return a supported space, creating and supporting one when needed."""
    supported_space_ids = _list_supported_space_ids(access_token)
    if supported_space_ids:
        return supported_space_ids[0]

    space_id = _get_or_create_user_space(access_token)
    _support_space(space_id, access_token)
    return _wait_for_supported_space(space_id, access_token)


def _upload_file(file_path: str, access_token: str, content: bytes) -> None:
    http_put(
        ip=docker_ip(ONEPROVIDER_CONTAINER_NAME),
        port=OP_REST_PORT,
        path=file_path,
        headers={
            **_authorization_headers(access_token),
            "Content-Type": "application/octet-stream",
        },
        data=content,
    )


def _download_file(file_path: str, access_token: str) -> bytes:
    return http_get(
        ip=docker_ip(ONEPROVIDER_CONTAINER_NAME),
        port=OP_REST_PORT,
        path=file_path,
        headers=_authorization_headers(access_token),
    ).content


def _remove_file(file_path: str, access_token: str) -> None:
    http_delete(
        ip=docker_ip(ONEPROVIDER_CONTAINER_NAME),
        port=OP_REST_PORT,
        path=file_path,
        headers=_authorization_headers(access_token),
    )


def upload_and_download_file(access_token: str, content: bytes) -> bytes:
    """Upload a temporary text file through REST and download its content."""
    space_id = get_or_create_supported_space(access_token)
    file_name = f"demo-mode-rest-{uuid4().hex}.txt"
    file_path = get_provider_rest_path("data", space_id, "path", file_name)

    _upload_file(file_path, access_token, content)
    try:
        return _download_file(file_path, access_token)
    finally:
        _remove_file(file_path, access_token)
