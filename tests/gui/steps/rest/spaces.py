"""Steps for spaces management using REST API."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Any

from tests import OZ_REST_PORT
from tests.conftest import Users
from tests.utils.rest_utils import get_zone_rest_path, http_delete, http_get


def get_user_spaces(zone_hostname: Any, user: Any, users: Users) -> Any:
    return http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces"),
        auth=(user, users[user].password),
    ).json()["spaces"]


def leave_user_space(zone_hostname: Any, user: Any, users: Users, space_id: Any) -> Any:
    http_delete(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces", space_id),
        auth=(user, users[user].password),
    )
