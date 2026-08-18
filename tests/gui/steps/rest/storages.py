"""Helpers for storages management using REST API."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from contextlib import suppress
from typing import Any

from tests import PANEL_REST_PORT
from tests.gui.conftest import WAIT_BACKEND
from tests.utils.http_exceptions import HTTPNotFound
from tests.utils.rest_utils import (
    get_panel_rest_path,
    http_delete,
    http_get,
    http_patch,
)
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


@repeat_failed(timeout=WAIT_BACKEND, exceptions=AssertionError)
def assert_storage_absence(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
) -> None:
    assert storage_id not in get_storages_ids(
        provider_hostname, onepanel_username, onepanel_password
    )


def remove_storage_by_id(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
) -> None:
    with suppress(HTTPNotFound):
        http_delete(
            ip=provider_hostname,
            port=PANEL_REST_PORT,
            path=get_panel_rest_path("provider", "storages", storage_id),
            auth=(onepanel_username, onepanel_password),
        )


def modify_storage_using_rest(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: str,
    storage_id: str,
    storage_data: dict[str, dict[str, Any]],
) -> None:
    http_patch(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "storages", storage_id),
        auth=(onepanel_username, onepanel_password),
        data=json.dumps(storage_data),
    )
