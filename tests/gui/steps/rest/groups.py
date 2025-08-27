"""Steps for groups management using REST API."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests import OZ_REST_PORT
from tests.utils.rest_utils import get_zone_rest_path, http_delete, http_get


def get_user_groups(zone_hostname, user, users):
    return http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "groups"),
        auth=(user, users[user].password),
    ).json()["groups"]


def leave_user_group(zone_hostname, user, users, group_id):
    http_delete(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "groups", group_id),
        auth=(user, users[user].password),
    )
