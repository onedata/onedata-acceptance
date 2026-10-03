"""Helpers for shares management using REST API."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json

from tests import OP_REST_PORT, OZ_REST_PORT
from tests.utils.rest_utils import (
    get_provider_rest_path,
    get_zone_rest_path,
    http_get,
    http_post,
    http_put,
)


def create_share_for_file_using_rest(
    provider_hostname: str,
    access_token: str,
    file_id: str,
    share_name: str,
) -> str:
    response = http_post(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("shares"),
        headers={"X-Auth-Token": access_token},
        data=json.dumps({"name": share_name, "fileId": file_id}),
    )
    share_id = response.json()["shareId"]
    if not isinstance(share_id, str):
        raise TypeError("Share creation response contains an invalid share ID")
    return share_id


def get_first_handle_service_id(
    zone_hostname: str,
    access_token: str,
) -> str:
    handle_service_id = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handle_services"),
        headers={"X-Auth-Token": access_token},
    ).json()["handle_services"][0]
    if not isinstance(handle_service_id, str):
        raise TypeError("Handle services response contains an invalid service ID")
    return handle_service_id


def add_user_to_handle_service_using_rest(
    zone_hostname: str,
    access_token: str,
    handle_service_id: str,
    user_id: str,
) -> None:
    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handle_services", handle_service_id, "users", user_id),
        headers={"X-Auth-Token": access_token},
    )
