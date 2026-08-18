"""Meta steps for space management using REST API helpers."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from contextlib import suppress

from tests import OZ_REST_PORT
from tests.gui.steps.rest.spaces import (
    get_space_details,
    get_supported_space_ids,
    revoke_space_support_using_rest,
)
from tests.utils.http_exceptions import HTTPNotFound, HTTPServerError
from tests.utils.rest_utils import get_zone_rest_path, http_delete


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
        space_details = get_space_details(
            provider_hostname, onepanel_username, onepanel_password, space_id
        )
        if space_details["storageId"] == storage_id:
            matching_space_ids.append(space_id)

    return matching_space_ids


def revoke_all_space_supports_using_rest(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
) -> None:
    for space_id in get_supported_space_ids(
        provider_hostname, onepanel_username, onepanel_password
    ):
        revoke_space_support_using_rest(
            provider_hostname, onepanel_username, onepanel_password, space_id
        )

    assert not get_supported_space_ids(
        provider_hostname, onepanel_username, onepanel_password
    )


def revoke_space_supports_for_storage_using_rest(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
) -> None:
    for space_id in get_space_ids_supported_by_storage(
        provider_hostname, onepanel_username, onepanel_password, storage_id
    ):
        # A space finalizer may have already removed the space in Onezone while
        # Onepanel still briefly lists its support. In that case Oneprovider
        # reports `not_found`, which Onepanel exposes as a server error. Treat
        # the revoke as idempotent and verify the resulting state below.
        with suppress(HTTPServerError):
            revoke_space_support_using_rest(
                provider_hostname, onepanel_username, onepanel_password, space_id
            )

    assert not get_space_ids_supported_by_storage(
        provider_hostname, onepanel_username, onepanel_password, storage_id
    )
