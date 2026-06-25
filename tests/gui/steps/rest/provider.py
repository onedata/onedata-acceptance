"""Steps for provider management using REST API."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"
import json

from requests import Response

from tests import ONES3_PORT, OP_REST_PORT, PANEL_REST_PORT
from tests.gui.type_definitions import ProviderResponse
from tests.gui.utils.generic import OnedataService
from tests.type_definitions import Hosts, JsonValue, Users
from tests.utils.bdd_utils import parsers, wt
from tests.utils.rest_utils import (
    get_panel_rest_path,
    get_provider_rest_path,
    http_get,
    http_patch,
    http_post,
)
from tests.utils.user_utils import AdminUser


def get_provider_id(provider: str, hosts: Hosts, users: Users) -> str:
    user = "admin"
    provider_hostname = hosts[provider]["hostname"]
    provider_conf = http_get(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("configuration"),
        auth=(user, users[user].password),
    ).json()
    return provider_conf["providerId"]


@wt(
    parsers.parse(
        "using REST, user {user} sees that status of OneS3 of {provider} is ok"
    )
)
def assert_provider_ones3_status_ok(provider: str, hosts: Hosts) -> None:
    provider_hostname = hosts[provider]["hostname"]
    status = http_get(
        ip=provider_hostname,
        port=ONES3_PORT,
        path="/.__onedata__status__",
    ).json()
    err_msg = f"Status of OneS3 is {status["isOk"]}"
    assert status["isOk"], err_msg


def add_provider_service_node(
    hosts: Hosts,
    provider: str,
    onepanel_credentials: AdminUser,
    data: dict[str, JsonValue],
    service: OnedataService,
) -> ProviderResponse:
    provider_hostname = hosts[provider]["hostname"]
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    res = http_post(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", service.value),
        headers={"Content-Type": "application/json"},
        auth=(onepanel_username, onepanel_password),
        data=json.dumps(data),
    )
    return res.json()


def get_provider_service_nodes_statuses(
    hosts: Hosts,
    provider: str,
    onepanel_credentials: AdminUser,
    service: OnedataService,
) -> ProviderResponse:
    provider_hostname = hosts[provider]["hostname"]
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    res = http_get(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", service.value),
        auth=(onepanel_username, onepanel_password),
    )
    return res.json()


def start_stop_provider_service_node(
    hosts: Hosts,
    host: str,
    provider: str,
    onepanel_credentials: AdminUser,
    service: OnedataService,
    start: bool = True,
) -> Response:
    provider_hostname = hosts[provider]["hostname"]
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    res = http_patch(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", service.value, host)
        + f"?started={"true" if start else "false"}",
        auth=(onepanel_username, onepanel_password),
    )
    return res
