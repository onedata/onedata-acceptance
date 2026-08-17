"""Steps for harvesters management using REST API."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests import OZ_REST_PORT
from tests.utils.rest_utils import get_zone_rest_path, http_get


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
