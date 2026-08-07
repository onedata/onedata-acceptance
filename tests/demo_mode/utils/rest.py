"""REST helpers for demo-mode tests."""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import cast

from tests import OZ_REST_PORT
from tests.type_definitions import JsonObject
from tests.utils.docker_utils import docker_ip
from tests.utils.rest_utils import get_zone_rest_path, http_get

ONEZONE_CONTAINER_NAME = "oz_test"


def get_onezone_configuration() -> JsonObject:
    """Get the public configuration exposed by the demo Onezone REST API."""
    response = http_get(
        ip=docker_ip(ONEZONE_CONTAINER_NAME),
        port=OZ_REST_PORT,
        path=get_zone_rest_path("configuration"),
    )
    return cast(JsonObject, response.json())
