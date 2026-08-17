"""Steps for harvesters management using REST API."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests import OZ_REST_PORT
from tests.utils.http_exceptions import HTTPNotFound
from tests.utils.rest_utils import get_zone_rest_path, http_delete, http_get


def get_user_harvester_ids(
    zone_hostname: str,
    username: str,
    password: str,
) -> set[str]:
    response = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "harvesters"),
        auth=(username, password),
    )

    return set(response.json()["harvesters"])


def remove_harvester_using_rest(
    harvester_id: str,
    zone_hostname: str,
    owner_username: str,
    owner_password: str,
) -> None:
    try:
        http_delete(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("harvesters", harvester_id),
            auth=(owner_username, owner_password),
        )
    except HTTPNotFound:
        # A scenario may explicitly remove the harvester before its finalizer runs.
        pass
