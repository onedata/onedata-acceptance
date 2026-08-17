"""Helpers for storages management using REST API."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from typing import Any

import yaml

from tests import PANEL_REST_PORT
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.common.miscellaneous import _camel_transform
from tests.gui.steps.rest.spaces import revoke_space_supports_for_storage_using_rest
from tests.type_definitions import Hosts
from tests.utils.rest_utils import (
    get_panel_rest_path,
    http_delete,
    http_get,
    http_patch,
)
from tests.utils.user_utils import User
from tests.utils.utils import repeat_failed


def get_storages_ids(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
) -> list[str]:
    return http_get(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "storages"),
        auth=(onepanel_username, onepanel_password),
    ).json()["ids"]


def get_storage_details(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
) -> dict[str, Any]:
    return http_get(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "storages", storage_id),
        auth=(onepanel_username, onepanel_password),
    ).json()


def remove_storage_by_id(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
) -> None:
    http_delete(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "storages", storage_id),
        auth=(onepanel_username, onepanel_password),
    )


def get_storage_ids_by_name(
    storage_name: str,
    provider: str,
    hosts: Hosts,
    onepanel_credentials: User,
) -> list[str]:
    provider_hostname = hosts[provider]["hostname"]
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    storage_ids = get_storages_ids(
        provider_hostname, onepanel_username, onepanel_password
    )
    selected_ids = []
    for storage_id in storage_ids:
        storage_details = get_storage_details(
            provider_hostname, onepanel_username, onepanel_password, storage_id
        )
        if storage_name == storage_details["name"]:
            selected_ids.append(storage_id)
    return selected_ids


@repeat_failed(timeout=WAIT_BACKEND)
def remove_storage_by_id_and_wait_until_absent(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
) -> None:
    storage_ids = get_storages_ids(
        provider_hostname, onepanel_username, onepanel_password
    )
    if storage_id not in storage_ids:
        return

    remove_storage_by_id(
        provider_hostname, onepanel_username, onepanel_password, storage_id
    )
    assert storage_id not in get_storages_ids(
        provider_hostname, onepanel_username, onepanel_password
    )


def restore_config_and_remove_storage_by_id(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
    storage_name: str,
    config: str,
) -> None:
    """Restore mutable storage parameters before removing the storage.

    Oneprovider caches storage helper parameters after the storage record is
    removed. Restoring the original parameters prevents a modified backend
    configuration from leaking into a consecutive test run.
    """
    if storage_id not in get_storages_ids(
        provider_hostname, onepanel_username, onepanel_password
    ):
        return

    storage_data = storage_data_from_config(config, storage_name)
    storage_config: dict[str, Any] = storage_data[storage_name]
    storage_config.pop("importedStorage", None)
    try:
        http_patch(
            ip=provider_hostname,
            port=PANEL_REST_PORT,
            path=get_panel_rest_path("provider", "storages", storage_id),
            auth=(onepanel_username, onepanel_password),
            data=json.dumps(storage_data),
        )
    finally:
        revoke_space_supports_for_storage_using_rest(
            provider_hostname, onepanel_username, onepanel_password, storage_id
        )
        remove_storage_by_id_and_wait_until_absent(
            provider_hostname, onepanel_username, onepanel_password, storage_id
        )


def storage_data_from_config(
    config: str, storage_name: str
) -> dict[str, dict[str, Any]]:
    storage_config: dict[str, object] = {}
    options = yaml.load(config, yaml.Loader)

    for key, val in options.items():
        if key == "storage type":
            storage_config["type"] = val.lower()
        elif key == "imported storage":
            storage_config["importedStorage"] = True
        else:
            storage_config[_camel_transform(key)] = val

    return {storage_name: storage_config}
