"""Steps for provider management using REST API."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"
import json
from typing import Any

from tests import ONES3_PORT, OP_REST_PORT, PANEL_REST_PORT
from tests.conftest import Hosts, Users
from tests.gui.utils.generic import OnedataService
from tests.utils.bdd_utils import parsers, wt
from tests.utils.rest_utils import (
    get_panel_rest_path,
    get_provider_rest_path,
    http_get,
    http_patch,
    http_post,
)


def get_provider_id(provider: Any, hosts: Hosts, users: Users) -> Any:
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
def assert_provider_ones3_status_ok(provider: Any, hosts: Hosts) -> Any:
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
    provider: Any,
    onepanel_credentials: Any,
    data: Any,
    service: OnedataService,
) -> Any:
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
    hosts: Hosts, provider: Any, onepanel_credentials: Any, service: OnedataService
) -> Any:
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
    host: Any,
    provider: Any,
    onepanel_credentials: Any,
    service: OnedataService,
    start: Any = True,
) -> Any:
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
