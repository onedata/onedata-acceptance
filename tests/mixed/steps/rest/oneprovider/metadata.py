"""Utils to facilitate metadata operations in Oneprovider using REST API."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import base64
import json

from oneprovider_client import CustomFileMetadataApi

from tests.gui.utils import CDMIClient as cdmi
from tests.mixed.type_definitions import HostsConfig
from tests.mixed.utils.common import login_to_provider
from tests.type_definitions import JsonValue
from tests.utils.user_utils import Users


def assert_metadata_in_op_rest(
    user: str,
    users: Users,
    host: str,
    hosts: HostsConfig,
    path: str,
    tab_name: str,
    val: str,
) -> None:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    metadata = client.read_metadata(path)["metadata"]
    if tab_name.lower() == "xattrs":
        attribute, val = val.split("=")
        assert attribute in metadata, f"{path} has no {attribute} {tab_name} metadata"
        assert (
            val == metadata[attribute]
        ), f"{path} has no {attribute} = {val} {tab_name}"
    else:
        metadata = metadata[f"onedata_{tab_name.lower()}"]
        if "onedata_base64" in metadata:

            metadata = metadata["onedata_base64"]
            metadata = base64.b64decode(metadata.encode("ascii")).decode("ascii")

        if tab_name.lower() == "json":
            assert val == json.dumps(
                metadata
            ), f'{path} has no {val} {tab_name} metadata but "{metadata}"'
        else:
            assert (
                val == metadata
            ), f'{path} has no {val} {tab_name} metadata but "{metadata}"'


def set_metadata_in_op_rest(
    user: str,
    users: Users,
    host: str,
    hosts: HostsConfig,
    path: str,
    tab_name: str,
    val: str,
) -> None:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    if tab_name == "xattrs":
        attribute, val = val.split("=")
    else:
        attribute = f"onedata_{tab_name.lower()}"
        if tab_name.lower() == "json":
            val = json.loads(val)
    client.write_metadata(path, {attribute: val})


def add_json_metadata_to_file_rest(
    user: str,
    users: Users,
    hosts: HostsConfig,
    host: str,
    expression: JsonValue,
    file_id: str,
) -> None:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    cfm_api = CustomFileMetadataApi(user_client_op)
    cfm_api.set_json_metadata(file_id, expression)


def remove_all_metadata_in_op_rest(
    user: str, users: Users, host: str, hosts: HostsConfig, path: str
) -> None:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    client.write_metadata(path, {})


def assert_no_such_metadata_in_op_rest(
    user: str,
    users: Users,
    host: str,
    hosts: HostsConfig,
    path: str,
    tab_name: str,
    val: str,
) -> None:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    metadata = client.read_metadata(path)["metadata"]
    if tab_name == "xattrs":
        attribute, val = val.split("=")
    else:
        attribute = f"onedata_{tab_name.lower()}"
    try:
        metadata = metadata[attribute]
    except KeyError:
        pass
    else:
        if tab_name.lower() == "json":
            expected_metadata = json.loads(val)
            for key in expected_metadata:
                assert (
                    key not in metadata or metadata[key] != expected_metadata[key]
                ), f"There is {expected_metadata} {tab_name} metadata"
        else:
            assert val != metadata, f"There is {val} {tab_name} metadata"
