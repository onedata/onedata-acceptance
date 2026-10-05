"""REST client for the demo-mode Onezone."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from dataclasses import dataclass
from typing import cast
from urllib.parse import urlsplit

from tests import OZ_REST_PORT
from tests.demo_mode.type_definitions import RestEndpoint
from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.rest.helpers import ONEZONE_URL_PREFIX, _authorization_headers
from tests.type_definitions import JsonObject
from tests.utils.rest_utils import get_zone_rest_path, http_get, http_post


@dataclass(frozen=True)
class OnezoneRestClient:
    """REST operations directed at the demo Onezone."""

    commands: DemoCommands
    access_token: str | None = None

    def _endpoint(self) -> RestEndpoint:
        command_output = self.commands.onezone_url().run()
        output_lines = command_output.splitlines()
        if len(output_lines) != 1 or not output_lines[0].startswith(ONEZONE_URL_PREFIX):
            raise AssertionError(
                f"The Onezone URL command returned unexpected output: {command_output!r}"
            )

        onezone_url = output_lines[0].removeprefix(ONEZONE_URL_PREFIX)
        if not onezone_url:
            raise AssertionError("The Onezone URL command returned an empty URL")

        try:
            parsed_url = urlsplit(onezone_url)
            hostname = parsed_url.hostname
            port = parsed_url.port or OZ_REST_PORT
        except ValueError as error:
            raise AssertionError(
                f"The Onezone URL command returned an invalid URL: {onezone_url!r}"
            ) from error

        assert parsed_url.scheme == "https", f"Expected an HTTPS Onezone URL, got {onezone_url!r}"
        assert hostname, f"Expected the Onezone URL to contain a hostname, got {onezone_url!r}"
        assert parsed_url.username is None, (
            f"Expected the Onezone URL not to contain a username, got {onezone_url!r}"
        )
        assert parsed_url.password is None, (
            f"Expected the Onezone URL not to contain a password, got {onezone_url!r}"
        )
        assert parsed_url.path in ("", "/"), (
            f"Expected the Onezone URL not to contain a path, got {onezone_url!r}"
        )
        assert not parsed_url.query, (
            f"Expected the Onezone URL not to contain a query, got {onezone_url!r}"
        )
        assert not parsed_url.fragment, (
            f"Expected the Onezone URL not to contain a fragment, got {onezone_url!r}"
        )
        return RestEndpoint(host=hostname, port=port)

    def _authenticated_headers(self) -> dict[str, str]:
        if self.access_token is None:
            raise ValueError("This Onezone REST operation requires an access token")
        return _authorization_headers(self.access_token)

    def configuration(self) -> JsonObject:
        endpoint = self._endpoint()
        response = http_get(
            ip=endpoint.host,
            port=endpoint.port,
            path=get_zone_rest_path("configuration"),
        )
        return cast(JsonObject, response.json())

    def create_space(self, *, name: str) -> str:
        endpoint = self._endpoint()
        response = http_post(
            ip=endpoint.host,
            port=endpoint.port,
            path=get_zone_rest_path("user", "spaces"),
            headers=self._authenticated_headers(),
            data=json.dumps({"name": name}),
        )
        location = response.headers.get("Location")
        if not location:
            raise AssertionError("Onezone did not return the created space location")
        return location.rstrip("/").rsplit("/", maxsplit=1)[-1]

    def create_space_support_token(self, *, space_id: str) -> str:
        endpoint = self._endpoint()
        response = http_post(
            ip=endpoint.host,
            port=endpoint.port,
            path=get_zone_rest_path("spaces", space_id, "providers", "token"),
            headers=self._authenticated_headers(),
        )
        response_body = cast(JsonObject, response.json())
        return cast(str, response_body["token"])
