"""Meta steps for harvester management using REST API helpers."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from contextlib import suppress

from tests import OZ_REST_PORT
from tests.utils.http_exceptions import HTTPNotFound
from tests.utils.rest_utils import get_zone_rest_path, http_delete


def remove_harvester_using_rest(
    harvester_id: str,
    zone_hostname: str,
    owner_username: str,
    owner_password: str,
) -> None:
    # A scenario may explicitly remove the harvester before its finalizer runs.
    with suppress(HTTPNotFound):
        http_delete(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("harvesters", harvester_id),
            auth=(owner_username, owner_password),
        )
