"""This module contains implementation of mixed oneclient steps for data
management.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import os
from collections.abc import Iterable, Mapping
from functools import partial
from typing import cast

import pytest
import yaml

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils.generic import parse_elements_sequence
from tests.mixed.utils.data import (
    Content,
    ContentItem,
    CreateItem,
    assert_ace,
    check_files_tree,
    create_content,
    get_acl_metadata,
)
from tests.oneclient.steps import (
    multi_dir_steps,
    multi_file_steps,
    multi_reg_file_steps,
)
from tests.type_definitions import EnvDesc, Hosts, JsonValue
from tests.utils.acceptance_utils import compare, failure, time_attr
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


def change_client_name_to_hostname(client_name: str) -> str:
    return client_name.replace("oneclient", "client")


@wt(parsers.parse("{user} mounts oneclient using received token"))
def mount_new_oneclient_with_token(
    user: str, hosts: Hosts, users: Users, env_desc: EnvDesc, tmp_memory: TmpMemory
) -> None:
    token = cast(Mapping[str, str], tmp_memory[user]["mailbox"])["token"]
    users[user].mount_client(
        "oneclient-1",
        "client1",
        cast(Mapping[str, Mapping[str, str]], hosts),
        env_desc,
        token,
    )


def mount_new_oneclient_with_token_fail(
    user: str,
    hosts: Hosts,
    users: Users,
    env_desc: EnvDesc,
    tmp_memory: TmpMemory,
    client: str = "oneclient",
) -> None:
    if "oneclient" in client:
        token = cast(Mapping[str, str], tmp_memory[user]["mailbox"])["token"]
        users[user].mount_client(
            "oneclient-1",
            "client1",
            cast(Mapping[str, Mapping[str, str]], hosts),
            env_desc,
            token,
        )
        failure(user, users)


def mount_new_oneclient_result(
    user: str,
    hosts: Hosts,
    users: Users,
    env_desc: EnvDesc,
    tmp_memory: TmpMemory,
    result: str,
    client: str = "oneclient",
) -> None:
    if result == "succeeds":
        mount_new_oneclient_with_token(user, hosts, users, env_desc, tmp_memory)
    else:
        mount_new_oneclient_with_token_fail(
            user, hosts, users, env_desc, tmp_memory, client=client
        )


def create_dir_in_op_oneclient(
    user: str, full_path: str, users: Users, result: str, host: str
) -> None:
    if result == "fails":
        multi_dir_steps.fail_to_create(user, full_path, host, users)
    else:
        multi_dir_steps.create(user, full_path, host, users)


def create_file_in_op_oneclient(
    user: str,
    path: str,
    users: Users,
    result: str,
    host: str,
    request: pytest.FixtureRequest,
) -> None:
    if result == "fails":
        multi_file_steps.create_reg_file_fail(user, path, host, users, request)
    else:
        multi_file_steps.create_reg_file(user, path, host, users, request)


def create_file_in_op_oneclient_with_tokens(
    user: str,
    hosts: Hosts,
    users: Users,
    env_desc: EnvDesc,
    tmp_memory: TmpMemory,
    result: str,
    full_path: str,
    client_lower: str,
    request: pytest.FixtureRequest,
) -> None:
    try:
        mount_new_oneclient_result(
            user, hosts, users, env_desc, tmp_memory, result, client="oneclient"
        )

        if result == "succeeds":
            oneclient_host = change_client_name_to_hostname(client_lower)
            create_file_in_op_oneclient(
                user, full_path, users, result, oneclient_host, request
            )
    except AssertionError as e:
        if result == "fails":
            oneclient_host = change_client_name_to_hostname(client_lower)
            create_file_in_op_oneclient(
                user, full_path, users, result, oneclient_host, request
            )
        else:
            raise e


def see_items_in_op_oneclient(
    items: list[str], space: str, user: str, users: Users, result: str, host: str
) -> None:
    for item in items:
        last_elem_in_path = os.path.basename(item)
        if last_elem_in_path.startswith("dir"):
            full_path = f"{space}/{item}"
            if result == "fails":
                multi_dir_steps.cannot_list_dir(user, full_path, host, users)
            else:
                multi_dir_steps.list_dir(user, full_path, host, users)
        else:
            if result == "fails":
                multi_file_steps.stat_absent(user, space, item, host, users)
            else:
                multi_file_steps.stat_present(user, space, item, host, users)


def assert_num_of_files_in_path_in_op_oneclient(
    num: int, path: str, user: str, users: Users, host: str
) -> None:
    items = multi_dir_steps.list_dirs_base(user, path, host, users)
    assert_msg = f"Expected exactly {num} items in {path} but found {len(items)} items"
    assert len(items) == num, assert_msg


def create_directory_structure_in_op_oneclient(
    user: str,
    users: Users,
    config: str,
    space: str,
    host: str,
    hosts: Hosts,
    request: pytest.FixtureRequest,
) -> None:
    items = cast(Iterable[ContentItem], yaml.load(config, yaml.Loader))
    cwd = space
    create_content(
        user,
        users,
        cwd,
        items,
        create_item_in_op_oneclient,
        host,
        hosts,
        request,
    )


def create_item_in_op_oneclient(
    user: str,
    users: Users,
    cwd: str,
    name: str,
    content: Content,
    create_item_fun: CreateItem,
    host: str,
    hosts: Hosts,
    request: pytest.FixtureRequest,
) -> None:
    if name.startswith("dir"):
        multi_dir_steps.create(user, f"{cwd}/{name}", host, users)
    else:
        multi_file_steps.create_reg_file(user, f"{cwd}/{name}", host, users, request)
    if not content:
        return
    cwd += "/" + name
    create_content(
        user,
        users,
        cwd,
        content,
        create_item_fun,
        host,
        hosts,
        request,
    )


def assert_file_content_in_op_oneclient(
    path: str, text: str, user: str, users: Users, host: str
) -> None:
    multi_reg_file_steps.read_text(user, text, path, host, users)


def ls_dir_in_op_oneclient(path: str, user: str, users: Users, host: str) -> list[str]:
    return multi_dir_steps.list_dirs_base(user, path, host, users)


def get_time_for_file_in_op_oneclient(
    users: Users, user: str, client_node: str, time_name: str, file: str
) -> float:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    attr = time_attr(time_name)
    file_path = client.absolute_path(file)
    stat_result = client.stat(file_path)
    file_time = getattr(stat_result, attr)
    return file_time


@repeat_failed(timeout=WAIT_BACKEND)
def compare_file_time_with_copied_time_in_op_oneclient(
    users: Users,
    user: str,
    client_node: str,
    time_name1: str,
    file: str,
    time2: float,
    time_name2: str,
    comparator: str,
) -> None:
    time1 = get_time_for_file_in_op_oneclient(
        users, user, client_node, time_name1, file
    )
    err_msg = (
        f"Time comparison failed. \nTime1: {time_name1} = {time1} \n"
        f"Time2: {time_name2} = {time2} \nComparator: {comparator}"
    )
    assert compare(time1, time2, comparator), err_msg


def assert_space_content_in_op_oneclient(
    config: str, space_name: str, user: str, users: Users, host: str
) -> None:
    cwd = space_name
    ls_fun = partial(ls_dir_in_op_oneclient, user=user, users=users, host=host)
    assert_file_content_fun = partial(
        assert_file_content_in_op_oneclient, user=user, users=users, host=host
    )
    is_dir_fun = partial(
        check_file_is_of_type_oc,
        file_type="directory",
        user=user,
        users=users,
        host=host,
    )
    check_files_tree(
        config,
        cwd,
        is_dir_fun,
        ls_fun,
        assert_file_content_fun,
    )


def delete_empty_directory_in_op_oneclient(
    path: str, user: str, users: Users, result: str, host: str
) -> None:
    if result == "fails":
        multi_dir_steps.fail_to_delete_empty(user, path, host, users)
    else:
        multi_dir_steps.delete_empty(user, path, host, users)


def copy_item_in_op_oneclient(
    item_type: str,
    src_path: str,
    dst_path: str,
    user: str,
    users: Users,
    host: str,
) -> None:
    if item_type == "directory":
        multi_dir_steps.copy_dir(user, src_path, dst_path, host, users)
    else:
        multi_reg_file_steps.copy_reg_file(user, src_path, dst_path, host, users)


def move_item_in_op_oneclient(
    user: str,
    src_path: str,
    dst_path: str,
    users: Users,
    result: str,
    host: str,
) -> None:
    if result == "fails":
        multi_file_steps.rename_fail(user, src_path, dst_path, host, users)
    else:
        multi_file_steps.rename(user, src_path, dst_path, host, users)


@repeat_failed(timeout=WAIT_BACKEND)
def assert_posix_permissions_in_op_oneclient(
    user: str, path: str, perm: str, host: str, users: Users
) -> None:
    multi_file_steps.check_mode(user, path, perm, host, users)


def set_posix_permissions_in_op_oneclient(
    user: str, path: str, perm: str, host: str, users: Users, result: str
) -> None:
    if result == "fails":
        multi_file_steps.change_mode_fail(user, path, perm, host, users)
    else:
        multi_file_steps.change_mode(user, path, perm, host, users)


def set_metadata_in_op_oneclient(
    attr_val: str, attr_type: str, path: str, user: str, users: Users, host: str
) -> None:
    if attr_type == "xattrs":
        attr, attr_val = attr_val.split("=")
    else:
        attr = f"onedata_{attr_type.lower()}"

    multi_file_steps.set_xattr(user, path, attr, attr_val, host, users)


def assert_metadata_in_op_oneclient(
    attr_val: str, attr_type: str, path: str, user: str, users: Users, host: str
) -> None:
    if attr_type == "xattrs":
        attr, val = attr_val.split("=")
        multi_file_steps.check_string_xattr(user, path, attr, val, host, users)
    elif attr_type.lower() == "json":
        multi_file_steps.check_json_xattr(
            user, path, "onedata_json", attr_val, host, users
        )
    else:
        multi_file_steps.check_string_xattr(
            user, path, "onedata_rdf", attr_val, host, users
        )


def remove_all_metadata_in_op_oneclient(
    user: str, users: Users, host: str, path: str
) -> None:
    multi_file_steps.remove_xattr(user, path, "onedata_rdf", host, users)
    multi_file_steps.remove_xattr(user, path, "onedata_json", host, users)
    multi_file_steps.remove_all_xattr(user, path, host, users)


def assert_no_such_metadata_in_op_oneclient(
    user: str, users: Users, host: str, path: str, tab_name: str, val: str
) -> None:
    metadata = multi_file_steps.get_metadata(user, path, host, users)
    if tab_name == "xattrs":
        attr, val = val.split("=")
    else:
        attr = f"onedata_{tab_name.lower()}"
    try:
        metadata_value = metadata[attr]
    except KeyError:
        pass
    else:
        if tab_name.lower() == "json":
            expected_metadata = cast(Mapping[str, JsonValue], json.loads(val))
            actual_metadata = cast(Mapping[str, JsonValue], json.loads(metadata_value))
            for key in expected_metadata:
                assert (
                    key not in actual_metadata
                    or actual_metadata[key] != expected_metadata[key]
                ), f"There is {expected_metadata} {tab_name} metadata"
        else:
            assert val != metadata_value, f"There is {val} {tab_name} metadata"


def assert_ace_in_op_oneclient(
    user: str,
    users: Users,
    host: str,
    path: str,
    num: str,
    priv: str,
    item_type: str,
    name: str,
    numerals: dict[str, int],
) -> None:
    ace = multi_file_steps.get_metadata(user, path, host, users)["cdmi_acl"]
    ace = json.loads(ace)[numerals[num]]
    assert_ace(parse_elements_sequence(priv), item_type, ace, name, num, path)


def grant_acl_privileges_in_op_oneclient(
    user: str,
    users: Users,
    host: str,
    path: str,
    priv: str,
    item_type: str,
    groups: Mapping[str, str],
    name: str,
) -> None:
    try:
        acl_json = multi_file_steps.get_metadata(user, path, host, users)["cdmi_acl"]
        acl = json.loads(acl_json)
    except KeyError:
        acl = []
    acl = get_acl_metadata(
        acl,
        parse_elements_sequence(priv),
        item_type,
        groups,
        name,
        users,
        path,
    )
    multi_file_steps.set_xattr(user, path, "cdmi_acl", json.dumps(acl), host, users)


def remove_file_in_op_oneclient(
    user: str, path: str, host: str, users: Users, res: str
) -> None:
    if res == "fails":
        multi_file_steps.delete_file_fail(user, path, host, users)
    else:
        multi_file_steps.delete_file(user, path, host, users)


@wt(parsers.re(r"(?P<user>\w+) lists children of (?P<name>.*)"))
def list_children_in_op_oneclient(name: str, user: str, users: Users) -> None:
    user1 = users[user]
    client = user1.clients["client1"]
    path = client.get_mount_path() + "/" + name
    client.ls(path=path)


@given(parsers.parse("{user} mounts oneclient using received token"))
def given_mount_new_oneclient_with_token(
    user: str, hosts: Hosts, users: Users, env_desc: EnvDesc, tmp_memory: TmpMemory
) -> None:
    mount_new_oneclient_with_token(user, hosts, users, env_desc, tmp_memory)


def check_file_is_of_type_oc(
    file: str, file_type: str, user: str, users: Users, host: str
) -> bool:
    try:
        multi_file_steps.check_type_impl(user, file, file_type, host, users)
    except AssertionError:
        return False
    return True
