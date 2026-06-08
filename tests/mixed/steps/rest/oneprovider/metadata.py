"""Utils to facilitate metadata operations in Oneprovider using REST API."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import base64
import json
from typing import Any

from oneprovider_client import CustomFileMetadataApi

from tests.gui.utils import CDMIClient as cdmi
from tests.mixed.utils.common import login_to_provider


def assert_metadata_in_op_rest(
    user: Any, users: Any, host: Any, hosts: Any, path: Any, tab_name: Any, val: Any
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    metadata = client.read_metadata(path)["metadata"]
    if tab_name.lower() == "xattrs":
        (attr, val) = val.split("=")
        assert attr in metadata, f"{path} has no {attr} {tab_name} metadata"
        assert val == metadata[attr], f"{path} has no {attr} = {val} {tab_name}"
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
    user: Any, users: Any, host: Any, hosts: Any, path: Any, tab_name: Any, val: Any
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    if tab_name == "xattrs":
        (attr, val) = val.split("=")
    else:
        attr = f"onedata_{tab_name.lower()}"
        if tab_name.lower() == "json":
            val = json.loads(val)
    client.write_metadata(path, {attr: val})


def add_json_metadata_to_file_rest(
    user: Any, users: Any, hosts: Any, host: Any, expression: Any, file_id: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    cfm_api = CustomFileMetadataApi(user_client_op)
    cfm_api.set_json_metadata(file_id, expression)


def remove_all_metadata_in_op_rest(
    user: Any, users: Any, host: Any, hosts: Any, path: Any
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    client.write_metadata(path, {})


def assert_no_such_metadata_in_op_rest(
    user: Any, users: Any, host: Any, hosts: Any, path: Any, tab_name: Any, val: Any
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    metadata = client.read_metadata(path)["metadata"]
    if tab_name == "xattrs":
        attr, val = val.split("=")
    else:
        attr = f"onedata_{tab_name.lower()}"
    try:
        metadata = metadata[attr]
    except KeyError:
        pass
    else:
        if tab_name.lower() == "json":
            val = json.loads(val)
            for key in val:
                assert (
                    key not in metadata or metadata[key] != val[key]
                ), f"There is {val} {tab_name} metadata"
        else:
            assert val != metadata, f"There is {val} {tab_name} metadata"
