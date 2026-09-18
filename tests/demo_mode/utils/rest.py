"""REST helpers for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from typing import Final, cast
from urllib.parse import urlsplit

from tests import OP_REST_PORT, OZ_REST_PORT, PANEL_REST_PORT
from tests.demo_mode.type_definitions import RestEndpoint
from tests.demo_mode.utils.command_runner import (
    assert_command_succeeded,
    run_command_and_wait_to_finish,
)
from tests.demo_mode.utils.command_templates import command_path
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

SPACE_SUPPORT_SIZE: Final = 1024**3
SPACE_APPEARANCE_TIMEOUT: Final = 60.0
ONEZONE_URL_PREFIX: Final = "URL: "


def _authorization_headers(access_token: str) -> dict[str, str]:
    return {"X-Auth-Token": access_token}


def _get_onezone_url() -> str:
    relative_command_path = "common/get_onezone_url.sh"
    command = command_path(relative_command_path).read_text(encoding="utf-8")
    result = run_command_and_wait_to_finish(
        command,
        relative_command_path,
        capture_output=True,
    )
    assert_command_succeeded(result, relative_command_path)

    output_lines = result.stdout.splitlines()
    if len(output_lines) != 1 or not output_lines[0].startswith(ONEZONE_URL_PREFIX):
        raise AssertionError(
            f"The Onezone URL command returned unexpected output: {result.stdout!r}"
        )

    onezone_url = output_lines[0].removeprefix(ONEZONE_URL_PREFIX)
    if not onezone_url:
        raise AssertionError("The Onezone URL command returned an empty URL")
    return onezone_url


def _get_onezone_rest_endpoint() -> RestEndpoint:
    onezone_url = _get_onezone_url()
    try:
        parsed_url = urlsplit(onezone_url)
        hostname = parsed_url.hostname
        port = parsed_url.port or OZ_REST_PORT
    except ValueError as error:
        raise AssertionError(
            f"The Onezone URL command returned an invalid URL: {onezone_url!r}"
        ) from error

    assert parsed_url.scheme == "https", (
        f"Expected an HTTPS Onezone URL, got {onezone_url!r}"
    )
    assert hostname, (
        f"Expected the Onezone URL to contain a hostname, got {onezone_url!r}"
    )
    assert parsed_url.username is None, (
        f"Expected the Onezone URL not to contain a username, got {onezone_url!r}"
    )
    assert parsed_url.password is None, (
        f"Expected the Onezone URL not to contain a password, got {onezone_url!r}"
    )
    assert parsed_url.path in ("", "/"), (
        f"Expected the Onezone URL not to contain a path, got {onezone_url!r}"
    )
    assert not parsed_url.query, (
        f"Expected the Onezone URL not to contain a query, got {onezone_url!r}"
    )
    assert not parsed_url.fragment, (
        f"Expected the Onezone URL not to contain a fragment, got {onezone_url!r}"
    )

    return RestEndpoint(host=hostname, port=port)


def get_onezone_configuration() -> JsonObject:
    """Get the public configuration exposed by the demo Onezone REST API."""
    endpoint = _get_onezone_rest_endpoint()
    response = http_get(
        ip=endpoint.host,
        port=endpoint.port,
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
    spaces = _list_accessible_spaces(provider_container, access_token)
    return [cast(str, space["spaceId"]) for space in spaces]


def _list_accessible_spaces(
    provider_container: str,
    access_token: str,
) -> list[JsonObject]:
    response = http_get(
        ip=docker_ip(provider_container),
        port=OP_REST_PORT,
        path=get_provider_rest_path("spaces"),
        headers=_authorization_headers(access_token),
    )
    return cast(list[JsonObject], response.json())


def _create_space(space_name: str, access_token: str) -> str:
    endpoint = _get_onezone_rest_endpoint()
    response = http_post(
        ip=endpoint.host,
        port=endpoint.port,
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
    endpoint = _get_onezone_rest_endpoint()
    response = http_post(
        ip=endpoint.host,
        port=endpoint.port,
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


def get_space_id(
    provider_container: str,
    space_name: str,
    access_token: str,
) -> str:
    """Return the ID of an accessible space with the requested name."""
    matching_space_ids = [
        cast(str, space["spaceId"])
        for space in _list_accessible_spaces(provider_container, access_token)
        if space.get("name") == space_name
    ]
    assert len(matching_space_ids) == 1, (
        f"Expected exactly one accessible space named {space_name!r} through "
        f"{provider_container}, got {len(matching_space_ids)}"
    )
    return matching_space_ids[0]


def create_and_support_space(
    provider_container: str,
    space_name: str,
    access_token: str,
) -> str:
    """Create a new user space and support it with the selected provider."""
    space_id = _create_space(space_name, access_token)
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


def upload_file(
    provider_container: str,
    space_id: str,
    file_name: str,
    access_token: str,
    content: bytes,
) -> None:
    """Upload a file that remains available for later assertions."""
    file_path = get_provider_rest_path("data", space_id, "path", file_name)
    _upload_file(provider_container, file_path, access_token, content)


def download_file(
    provider_container: str,
    space_id: str,
    file_name: str,
    access_token: str,
) -> bytes:
    """Download an existing file without removing it."""
    file_path = get_provider_rest_path("data", space_id, "path", file_name)
    return _download_file(provider_container, file_path, access_token)


def remove_file(
    provider_container: str,
    space_id: str,
    file_name: str,
    access_token: str,
) -> None:
    """Remove an existing file."""
    file_path = get_provider_rest_path("data", space_id, "path", file_name)
    _remove_file(provider_container, file_path, access_token)
