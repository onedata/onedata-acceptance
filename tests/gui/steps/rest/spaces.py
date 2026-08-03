"""Steps for spaces management using REST API."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests import OZ_REST_PORT
from tests.utils.rest_utils import get_zone_rest_path, http_delete, http_get
from tests.utils.user_utils import Users


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


def delete_space_with_rest(
    zone_hostname: str, owner_username: str, owner_password: str | None, space_id: str
) -> None:
    res = http_delete(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("spaces", space_id),
        auth=(owner_username, owner_password),
    )
    print(res.status_code, res.text)
