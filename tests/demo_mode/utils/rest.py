"""REST helpers for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from time import monotonic, sleep
from typing import Final, cast
from uuid import uuid4

from tests import OP_REST_PORT, OZ_REST_PORT, PANEL_REST_PORT
from tests.type_definitions import JsonObject, JsonValue
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


def _json_object(value: JsonValue, description: str) -> JsonObject:
    if not isinstance(value, dict):
        raise AssertionError(f"Expected {description} to be a JSON object")
    return value


def _json_string(value: JsonValue, description: str) -> str:
    if not isinstance(value, str) or not value:
        raise AssertionError(f"Expected {description} to be a non-empty string")
    return value


def _json_string_list(value: JsonValue, description: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise AssertionError(f"Expected {description} to be a list of strings")
    return cast(list[str], value)


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
    spaces = response.json()
    if not isinstance(spaces, list):
        raise AssertionError("Expected Oneprovider spaces to be a JSON list")

    return [
        _json_string(
            _json_object(space, "Oneprovider space").get("spaceId"),
            "Oneprovider space ID",
        )
        for space in spaces
    ]


def _list_user_space_ids(access_token: str) -> list[str]:
    response = http_get(
        ip=docker_ip(ONEZONE_CONTAINER_NAME),
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces"),
        headers=_authorization_headers(access_token),
    )
    response_body = _json_object(response.json(), "Onezone spaces response")
    return _json_string_list(response_body.get("spaces"), "Onezone space IDs")


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


def _support_space(space_id: str, access_token: str) -> None:
    provider_ip = docker_ip(ONEPROVIDER_CONTAINER_NAME)
    headers = _authorization_headers(access_token)
    supported_spaces_response = http_get(
        ip=provider_ip,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "spaces"),
        headers=headers,
    )
    supported_spaces = _json_object(
        supported_spaces_response.json(), "Onepanel spaces response"
    )
    supported_space_ids = _json_string_list(
        supported_spaces.get("ids"), "Onepanel space IDs"
    )
    if space_id in supported_space_ids:
        return

    support_token_response = http_post(
        ip=docker_ip(ONEZONE_CONTAINER_NAME),
        port=OZ_REST_PORT,
        path=get_zone_rest_path("spaces", space_id, "providers", "token"),
        headers=headers,
    )
    support_token_body = _json_object(
        support_token_response.json(), "space support token response"
    )
    support_token = _json_string(support_token_body.get("token"), "space support token")

    storages_response = http_get(
        ip=provider_ip,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "storages"),
        headers=headers,
    )
    storages = _json_object(storages_response.json(), "Onepanel storages response")
    storage_ids = _json_string_list(storages.get("ids"), "Onepanel storage IDs")
    if not storage_ids:
        raise AssertionError("Demo Oneprovider has no storage available")

    http_post(
        ip=provider_ip,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "spaces"),
        headers=headers,
        data=json.dumps(
            {
                "token": support_token,
                "size": SPACE_SUPPORT_SIZE,
                "storageId": storage_ids[0],
            }
        ),
    )


def get_or_create_supported_space(access_token: str) -> str:
    """Return a supported space, creating and supporting one when needed."""
    supported_space_ids = _list_supported_space_ids(access_token)
    if supported_space_ids:
        return supported_space_ids[0]

    user_space_ids = _list_user_space_ids(access_token)
    space_id = user_space_ids[0] if user_space_ids else _create_space(access_token)
    _support_space(space_id, access_token)

    deadline = monotonic() + SPACE_APPEARANCE_TIMEOUT
    while monotonic() < deadline:
        supported_space_ids = _list_supported_space_ids(access_token)
        if space_id in supported_space_ids:
            return space_id
        sleep(1)

    raise AssertionError(
        f"Space {space_id} did not appear in Oneprovider within "
        f"{SPACE_APPEARANCE_TIMEOUT:g}s"
    )


def upload_and_download_file(access_token: str, content: bytes) -> bytes:
    """Upload a temporary text file through REST and download its content."""
    provider_ip = docker_ip(ONEPROVIDER_CONTAINER_NAME)
    space_id = get_or_create_supported_space(access_token)
    file_name = f"demo-mode-rest-{uuid4().hex}.txt"
    file_path = get_provider_rest_path("data", space_id, "path", file_name)
    headers = {
        **_authorization_headers(access_token),
        "Content-Type": "application/octet-stream",
    }

    http_put(
        ip=provider_ip,
        port=OP_REST_PORT,
        path=file_path,
        headers=headers,
        data=content,
    )
    try:
        return http_get(
            ip=provider_ip,
            port=OP_REST_PORT,
            path=file_path,
            headers=_authorization_headers(access_token),
        ).content
    finally:
        http_delete(
            ip=provider_ip,
            port=OP_REST_PORT,
            path=file_path,
            headers=_authorization_headers(access_token),
        )
