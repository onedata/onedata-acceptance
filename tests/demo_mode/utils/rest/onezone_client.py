"""REST client for the demo-mode Onezone."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from dataclasses import dataclass
from typing import cast

from tests import OZ_REST_PORT
from tests.demo_mode.utils.rest.helpers import _authorization_headers
from tests.type_definitions import JsonObject
from tests.utils.rest_utils import get_zone_rest_path, http_get, http_post


@dataclass(frozen=True)
class OnezoneRestClient:
    """REST operations directed at the demo Onezone."""

    host: str
    access_token: str | None = None

    def _authenticated_headers(self) -> dict[str, str]:
        if self.access_token is None:
            raise ValueError("This Onezone REST operation requires an access token")
        return _authorization_headers(self.access_token)

    def configuration(self) -> JsonObject:
        response = http_get(
            ip=self.host,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("configuration"),
        )
        return cast(JsonObject, response.json())

    def create_space(self, *, name: str) -> str:
        response = http_post(
            ip=self.host,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("user", "spaces"),
            headers=self._authenticated_headers(),
            data=json.dumps({"name": name}),
        )
        location = response.headers.get("Location")
        if not location:
            raise AssertionError("Onezone did not return the created space location")
        return location.rstrip("/").rsplit("/", maxsplit=1)[-1]

    def create_space_support_token(self, *, space_id: str) -> str:
        response = http_post(
            ip=self.host,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("spaces", space_id, "providers", "token"),
            headers=self._authenticated_headers(),
        )
        response_body = cast(JsonObject, response.json())
        return cast(str, response_body["token"])
