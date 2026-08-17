"""Steps for groups management using REST API."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from contextlib import suppress

from tests import OZ_REST_PORT
from tests.utils.http_exceptions import HTTPNotFound
from tests.utils.rest_utils import get_zone_rest_path, http_delete, http_get
from tests.utils.user_utils import Users


def get_user_groups(zone_hostname: str, user: str, users: Users) -> list[str]:
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


def ensure_absence_of_group_using_rest(
    zone_hostname: str,
    admin_username: str,
    admin_password: str,
    group_id: str,
) -> None:
    with suppress(HTTPNotFound):
        http_delete(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("groups", group_id),
            auth=(admin_username, admin_password),
        )
