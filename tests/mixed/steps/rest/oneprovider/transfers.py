"""Utils to facilitate transfers operations in Oneprovider using REST API."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Mapping
from typing import Optional, cast

import yaml
from oneprovider_client import TransferApi

from tests import OP_REST_PORT
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.rest.provider import get_provider_id
from tests.mixed.steps.rest.oneprovider.data import _lookup_file_id
from tests.mixed.type_definitions import IdMap
from tests.mixed.utils.common import login_to_provider
from tests.type_definitions import Hosts, JsonObject, Users
from tests.utils.rest_utils import get_provider_rest_path, http_get
from tests.utils.utils import repeat_failed


def create_transfer_rest(
    user: str,
    users: Users,
    host: str,
    hosts: Hosts,
    transfer_type: str,
    path: str,
    replicating_provider: Optional[str] = None,
    evicting_provider: Optional[str] = None,
) -> None:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    transfer_api = TransferApi(client)
    file_id = _lookup_file_id(path, client)
    data = {"type": transfer_type, "dataSourceType": "file", "fileId": file_id}
    if replicating_provider:
        replicating_provider_id = get_provider_id(replicating_provider, hosts, users)
        data.update({"replicatingProviderId": replicating_provider_id})
    if evicting_provider:
        evicting_provider_id = get_provider_id(evicting_provider, hosts, users)
        data.update({"evictingProviderId": evicting_provider_id})
    transfer_api.create_transfer(data=data)


@repeat_failed(timeout=WAIT_BACKEND)
def get_recent_transfer_status_rest(
    user: str, users: Users, host: str, hosts: Hosts, space_id: str
) -> JsonObject:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    transfer_api = TransferApi(client)
    tid = transfer_api.get_all_transfers(space_id, state="ended").transfers[0]
    provider_hostname = hosts[host]["hostname"]
    res = http_get(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("transfers", tid),
        headers={"X-Auth-Token": users[user].token},
    )
    return cast(JsonObject, res.json())


def assert_recent_transfer_details_rest(
    user: str,
    users: Users,
    host: str,
    hosts: Hosts,
    space: str,
    spaces: IdMap,
    config: str,
) -> None:
    transfer_status = get_recent_transfer_status_rest(
        user, users, host, hosts, spaces[space]
    )
    details = cast(Mapping[str, str], yaml.load(config, yaml.Loader))
    err_msg = "expected {} to be {} but got {}"
    for k, v in details.items():
        if k == "name":
            path = space + "/" + str(v)
            client = login_to_provider(user, users, hosts[host]["hostname"])
            expected_id = _lookup_file_id(path, client)
            assert transfer_status["fileId"] == expected_id, err_msg.format(
                "fileId", expected_id, transfer_status["fileId"]
            )
        if k == "replicated":
            # expecting value to be in MiB
            val = float(v.split(" ")[0]) * 1024 * 1024
            assert transfer_status["bytesReplicated"] == val, err_msg.format(
                "bytesReplicated", val, transfer_status["bytesReplicated"]
            )
        if k == "status":
            assert transfer_status["transferStatus"] == v, err_msg.format(
                k, v, transfer_status["transferStatus"]
            )
        if k == "type":
            assert transfer_status[k] == v, err_msg.format(k, v, transfer_status[k])


@repeat_failed(timeout=WAIT_BACKEND * 4)
def assert_recent_transfer_finished_rest(
    user: str,
    users: Users,
    host: str,
    hosts: Hosts,
    spaces: IdMap,
    space: str,
) -> None:
    transfer_status = get_recent_transfer_status_rest(
        user, users, host, hosts, spaces[space]
    )
    finished_statutes = ["skipped", "completed", "cancelled", "failed"]
    err_msg = (
        f"transfer status {transfer_status['transferStatus']} is not in one of finished"
        " states"
    )
    assert transfer_status["transferStatus"] in finished_statutes, err_msg
