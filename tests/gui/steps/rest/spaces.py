"""Steps for spaces management using REST API."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from contextlib import suppress
from typing import Any

from tests import OP_REST_PORT, OZ_REST_PORT
from tests.gui.constants import WAIT_BACKEND
from tests.utils.http_exceptions import HTTPNotFound
from tests.utils.rest_utils import (
    get_panel_rest_path,
    get_zone_rest_path,
    http_delete,
    http_get,
)
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


def get_supported_space_ids(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
) -> list[str]:
    return http_get(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_panel_rest_path("provider", "spaces"),
        auth=(onepanel_username, onepanel_password),
    ).json()["ids"]


def get_space_details(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    space_id: str,
) -> dict[str, Any]:
    return http_get(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_panel_rest_path("provider", "spaces", space_id),
        auth=(onepanel_username, onepanel_password),
    ).json()


def revoke_space_support_using_rest(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    space_id: str,
) -> None:
    with suppress(HTTPNotFound):
        http_delete(
            ip=provider_hostname,
            port=OP_REST_PORT,
            path=get_panel_rest_path("provider", "spaces", space_id),
            auth=(onepanel_username, onepanel_password),
        )


def get_user_spaces(zone_hostname: str, user: str, users: Users) -> list[str]:
    return http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces"),
        auth=(user, users[user].password),
    ).json()["spaces"]


def leave_user_space(
    zone_hostname: str, user: str, users: Users, space_id: str
) -> None:
    http_delete(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces", space_id),
        auth=(user, users[user].password),
    )


def delete_space_if_present_using_rest(
    zone_hostname: str, owner_username: str, owner_password: str, space_id: str
) -> None:
    with suppress(HTTPNotFound):
        http_delete(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("spaces", space_id),
            auth=(owner_username, owner_password),
        )


def get_space_ids_supported_by_storage(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
) -> list[str]:
    matching_space_ids = []
    for space_id in get_supported_space_ids(
        provider_hostname, onepanel_username, onepanel_password
    ):
        # The space may disappear between listing it and fetching its details.
        with suppress(HTTPNotFound):
            space_details = get_space_details(
                provider_hostname, onepanel_username, onepanel_password, space_id
            )
            if space_details["storageId"] == storage_id:
                matching_space_ids.append(space_id)

    return matching_space_ids


@repeat_failed(timeout=WAIT_BACKEND)
def assert_no_space_supports_using_rest(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
) -> None:
    assert not get_supported_space_ids(
        provider_hostname, onepanel_username, onepanel_password
    )


@repeat_failed(timeout=WAIT_BACKEND)
def assert_no_space_supports_for_storage_using_rest(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
) -> None:
    assert not get_space_ids_supported_by_storage(
        provider_hostname, onepanel_username, onepanel_password, storage_id
    )
