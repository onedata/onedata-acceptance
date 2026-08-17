"""Meta steps for group management using REST API helpers."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from contextlib import suppress

from tests import OZ_REST_PORT
from tests.utils.http_exceptions import HTTPNotFound
from tests.utils.rest_utils import get_zone_rest_path, http_delete


def delete_group_if_present_using_rest(
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
