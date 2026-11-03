"""REST client for a demo-mode Oneprovider."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from dataclasses import dataclass
from typing import cast

from tests import OP_REST_PORT, PANEL_REST_PORT
from tests.demo_mode.utils.rest.helpers import (
    SPACE_APPEARANCE_TIMEOUT,
    SPACE_SUPPORT_SIZE,
)
from tests.demo_mode.utils.rest.onezone_client import OnezoneRestClient
from tests.type_definitions import JsonObject
from tests.utils.rest_utils import (
    get_panel_rest_path,
    get_provider_rest_path,
    http_delete,
    http_get,
    http_post,
    http_put,
)
from tests.utils.utils import repeat_failed


@dataclass(frozen=True)
class OneproviderRestClient:
    """REST and Onepanel operations directed at one demo Oneprovider."""

    host: str
    access_token: str | None = None

    def configuration(self) -> JsonObject:
        response = http_get(
            ip=self.host,
            port=OP_REST_PORT,
            path=get_provider_rest_path("configuration"),
        )
        return cast(JsonObject, response.json())

    def supported_space_ids(self) -> list[str]:
        return self._list_onepanel_resource_ids("spaces")

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

    def create_and_support_space(
        self,
        onezone: OnezoneRestClient,
        *,
        name: str,
    ) -> str:
        space_id = onezone.create_space(name=name)
        if space_id not in self.supported_space_ids():
            storage_ids = self._list_onepanel_resource_ids("storages")
            if not storage_ids:
                raise AssertionError("Demo Oneprovider has no storage available")
            self._submit_space_support(
                support_token=onezone.create_space_support_token(space_id=space_id),
                storage_id=storage_ids[0],
            )
        return self._wait_for_accessible_space(space_id)

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

    def remove(self, *, space_id: str, file_name: str) -> None:
        file_path = get_provider_rest_path("data", space_id, "path", file_name)
        http_delete(
            ip=self.host,
            port=OP_REST_PORT,
            path=file_path,
            headers=self._authenticated_headers(),
        )

    def _authenticated_headers(self) -> dict[str, str]:
        if self.access_token is None:
            raise ValueError("This Oneprovider REST operation requires an access token")
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

    def _submit_space_support(
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

    @repeat_failed(
        timeout=SPACE_APPEARANCE_TIMEOUT,
        interval=1,
        exceptions=AssertionError,
    )
    def _wait_for_accessible_space(self, space_id: str) -> str:
        accessible_space_ids = [
            cast(str, space["spaceId"]) for space in self._list_accessible_spaces()
        ]
        assert space_id in accessible_space_ids, f"Space {space_id} has not appeared at {self.host}"
        return space_id
