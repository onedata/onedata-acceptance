"""Steps for groups management using REST API."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import List

from tests import OZ_REST_PORT
from tests.utils.rest_utils import get_zone_rest_path, http_delete, http_get
from tests.utils.user_utils import Users


def get_user_groups(zone_hostname: str, user: str, users: Users) -> List[str]:
    return http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "groups"),
        auth=(user, users[user].password),
    ).json()["groups"]


def leave_user_group(
    zone_hostname: str, user: str, users: Users, group_id: str
) -> None:
    http_delete(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "groups", group_id),
        auth=(user, users[user].password),
    )
