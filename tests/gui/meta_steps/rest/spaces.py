"""Meta steps for space management using REST API helpers."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from contextlib import suppress

from tests import OZ_REST_PORT
from tests.gui.steps.rest.spaces import (
    assert_no_space_supports_for_storage_using_rest,
    get_space_ids_supported_by_storage,
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
        # TODO: VFS-13774 Replace with HTTPNotFound once Onepanel returns 404
        # for revoked space support instead of 500 when space does not exist
        with suppress(HTTPServerError):
            revoke_space_support_using_rest(
                provider_hostname, onepanel_username, onepanel_password, space_id
            )

    assert_no_space_supports_for_storage_using_rest(
        provider_hostname, onepanel_username, onepanel_password, storage_id
    )
