"""REST client for the demo-mode Onezone."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from dataclasses import dataclass
from typing import cast

from tests import OZ_REST_PORT
from tests.type_definitions import JsonObject
from tests.utils.rest_utils import get_zone_rest_path, http_post


@dataclass(frozen=True)
class OnezoneRestClient:
    """REST operations directed at the demo Onezone."""

    host: str
    access_token: str

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

    def _authenticated_headers(self) -> dict[str, str]:
        return {"X-Auth-Token": self.access_token}
