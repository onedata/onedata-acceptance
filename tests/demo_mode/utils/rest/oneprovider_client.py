"""REST client for a demo-mode Oneprovider."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from dataclasses import dataclass
from typing import Final, cast

from tests import OP_REST_PORT, PANEL_REST_PORT
from tests.type_definitions import JsonObject
from tests.utils.rest_utils import (
    get_panel_rest_path,
    get_provider_rest_path,
    http_get,
    http_post,
    http_put,
)

SPACE_SUPPORT_SIZE: Final = 1024**3


@dataclass(frozen=True)
class OneproviderRestClient:
    """REST and Onepanel operations directed at one demo Oneprovider."""

    host: str
    access_token: str

    def supported_space_ids(self) -> list[str]:
        return self._list_onepanel_resource_ids("spaces")

    def storage_ids(self) -> list[str]:
        return self._list_onepanel_resource_ids("storages")

    def accessible_space_ids(self) -> list[str]:
        return [cast(str, space["spaceId"]) for space in self._list_accessible_spaces()]

    def space_id(self, *, name: str) -> str:
        matching_space_ids = [
            cast(str, space["spaceId"])
            for space in self._list_accessible_spaces()
            if space.get("name") == name
        ]
        assert len(matching_space_ids) == 1, (
            f"Expected exactly one accessible space named {name!r} through "
            f"{self.host}, got {len(matching_space_ids)}"
        )
        return matching_space_ids[0]

    def support_space(
        self,
        *,
        support_token: str,
        storage_id: str,
    ) -> None:
        http_post(
            ip=self.host,
            port=PANEL_REST_PORT,
            path=get_panel_rest_path("provider", "spaces"),
            headers=self._authenticated_headers(),
            data=json.dumps(
                {
                    "token": support_token,
                    "size": SPACE_SUPPORT_SIZE,
                    "storageId": storage_id,
                }
            ),
        )

    def upload(self, *, space_id: str, file_name: str, content: bytes) -> None:
        file_path = get_provider_rest_path("data", space_id, "path", file_name)
        http_put(
            ip=self.host,
            port=OP_REST_PORT,
            path=file_path,
            headers={
                **self._authenticated_headers(),
                "Content-Type": "application/octet-stream",
            },
            data=content,
        )

    def download(self, *, space_id: str, file_name: str) -> bytes:
        file_path = get_provider_rest_path("data", space_id, "path", file_name)
        return http_get(
            ip=self.host,
            port=OP_REST_PORT,
            path=file_path,
            headers=self._authenticated_headers(),
        ).content

    def _authenticated_headers(self) -> dict[str, str]:
        return {"X-Auth-Token": self.access_token}

    def _list_onepanel_resource_ids(self, resource: str) -> list[str]:
        response = http_get(
            ip=self.host,
            port=PANEL_REST_PORT,
            path=get_panel_rest_path("provider", resource),
            headers=self._authenticated_headers(),
        )
        response_body = cast(JsonObject, response.json())
        return cast(list[str], response_body["ids"])

    def _list_accessible_spaces(self) -> list[JsonObject]:
        response = http_get(
            ip=self.host,
            port=OP_REST_PORT,
            path=get_provider_rest_path("spaces"),
            headers=self._authenticated_headers(),
        )
        return cast(list[JsonObject], response.json())


def get_oneprovider_configuration(host: str) -> JsonObject:
    """Return the public configuration exposed by a Oneprovider."""
    response = http_get(
        ip=host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("configuration"),
    )
    return cast(JsonObject, response.json())
