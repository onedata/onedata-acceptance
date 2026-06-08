"""Utils to facilitate data operations in Oneprovider using REST API."""

__author__ = "Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from datetime import datetime
from functools import partial
from typing import Any

import pytest
import yaml
from cdmi_client import ContainerApi, DataObjectApi
from cdmi_client.rest import ApiException as CdmiException
from oneprovider_client import (
    BasicFileOperationsApi,
    FilePathResolutionApi,
    ShareApi,
    SpaceApi,
)
from oneprovider_client.rest import ApiException as OPException

from tests import OP_REST_PORT
from tests.gui.utils import CDMIClient as cdmi
from tests.gui.utils.generic import parse_seq
from tests.mixed.steps.rest.oneprovider.basic import see_item_is_dir_op_rest
from tests.mixed.utils.common import login_to_cdmi, login_to_provider
from tests.mixed.utils.data import (
    assert_ace,
    check_files_tree,
    create_content,
    get_acl_metadata,
)
from tests.utils.acceptance_utils import compare, time_attr
from tests.utils.http_exceptions import HTTPError
from tests.utils.rest_utils import get_provider_rest_path, http_post


def _lookup_file_id(path: Any, user_client_op: Any) -> Any:
    resolve_file_path_api = FilePathResolutionApi(user_client_op)
    file_id = resolve_file_path_api.lookup_file_id(path).file_id
    return file_id


def _read_file(path: Any, user: Any, users: Any, provider: Any, hosts: Any) -> Any:
    cli = login_to_cdmi(user, users, hosts[provider]["hostname"])
    dao = DataObjectApi(cli)
    return dao.read_data_object(path)


def _list_files(path: Any, user: Any, users: Any, provider: Any, hosts: Any) -> Any:
    user_client_op = login_to_provider(user, users, hosts[provider]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    file_id = _lookup_file_id(path, user_client_op)
    return [file.name for file in file_api.list_children(file_id).children]


def assert_file_content_in_op_rest(
    path: Any, text: Any, user: Any, users: Any, provider: Any, hosts: Any
) -> Any:
    file_content = _read_file(path, user, users, provider, hosts)
    assert_msg = (
        f"Expected file named {path} content to be {text} but found {file_content}"
    )
    assert file_content == text, assert_msg


def assert_space_content_in_op_rest(
    user: Any,
    users: Any,
    hosts: Any,
    config: Any,
    space_name: Any,
    _spaces: Any,
    host: Any,
) -> Any:
    cwd = "/" + space_name
    ls_fun = partial(_list_files, user=user, users=users, provider=host, hosts=hosts)
    assert_file_content_fun = partial(
        assert_file_content_in_op_rest,
        user=user,
        users=users,
        provider=host,
        hosts=hosts,
    )
    is_dir_fun = partial(
        see_item_is_dir_op_rest, user=user, users=users, host=host, hosts=hosts
    )
    check_files_tree(config, cwd, is_dir_fun, ls_fun, assert_file_content_fun)


def assert_num_of_files_in_path_in_op_rest(
    num: Any, path: Any, user: Any, users: Any, host: Any, hosts: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    file_id = _lookup_file_id(path, user_client_op)
    children = file_api.list_children(file_id).children
    assert_msg = (
        f"Expected exactly {num} items in {path} but found {len(children)} items"
    )
    assert num == len(children), assert_msg


def create_dir_in_op_rest(
    user: Any, users: Any, host: Any, hosts: Any, path: Any, result: Any
) -> Any:
    client = login_to_cdmi(user, users, hosts[host]["hostname"])

    c_api = ContainerApi(client)
    if result == "fails":
        with pytest.raises(CdmiException):
            c_api.create_container(path)
    else:
        c_api.create_container(path)


def remove_dir_in_op_rest(
    user: Any, users: Any, host: Any, hosts: Any, path: Any
) -> Any:
    client = login_to_cdmi(user, users, hosts[host]["hostname"])

    c_api = ContainerApi(client)
    c_api.delete_container(path)


def create_file_in_op_rest(
    user: Any,
    users: Any,
    host: Any,
    hosts: Any,
    path: Any,
    result: Any,
    access_token: Any = None,
    identity_token: Any = None,
) -> Any:
    client = login_to_cdmi(
        user,
        users,
        hosts[host]["hostname"],
        access_token=access_token,
        identity_token=identity_token,
    )

    do_api = DataObjectApi(client)
    if result == "fails":
        with pytest.raises(CdmiException):
            do_api.create_data_object(path, "")
    else:
        do_api.create_data_object(path, "")


def remove_file_in_op_rest(
    user: Any, users: Any, host: Any, hosts: Any, path: Any, result: Any
) -> Any:
    client = login_to_cdmi(user, users, hosts[host]["hostname"])

    do_api = DataObjectApi(client)
    if result == "fails":
        with pytest.raises(CdmiException):
            do_api.delete_data_object(path)
    else:
        do_api.delete_data_object(path)


def remove_file_using_token_in_op_rest(
    user: Any,
    users: Any,
    host: Any,
    hosts: Any,
    path: Any,
    result: Any,
    tmp_memory: Any,
) -> Any:
    access_token = tmp_memory[user]["mailbox"].get("token", None)
    client = login_to_cdmi(
        user, users, hosts[host]["hostname"], access_token=access_token
    )
    do_api = DataObjectApi(client)
    if result == "fails":
        with pytest.raises(CdmiException):
            do_api.delete_data_object(path)
    else:
        do_api.delete_data_object(path)


def see_items_in_op_rest(
    user: Any,
    users: Any,
    host: Any,
    hosts: Any,
    path_list: Any,
    result: Any,
    space: Any,
) -> Any:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(client)
    for path in parse_seq(path_list):
        path = f"{space}/{path}"
        check_if_item_exists_or_not_exists(result, path, client, file_api)


def see_item_in_op_rest_using_token(
    user: Any,
    name: Any,
    space: Any,
    host: Any,
    tmp_memory: Any,
    users: Any,
    hosts: Any,
    result: Any,
) -> Any:
    path = f"{space}/{name}"
    access_token = tmp_memory[user]["mailbox"].get("token", None)
    client = login_to_provider(
        user, users, hosts[host]["hostname"], access_token=access_token
    )
    file_api = BasicFileOperationsApi(client)
    check_if_item_exists_or_not_exists(result, path, client, file_api)


def check_if_item_id_in_items(path: Any, client: Any, file_api: Any) -> Any:
    file_id = _lookup_file_id(path, client)
    file_api.list_children(file_id)


def check_if_item_exists_or_not_exists(
    result: Any, path: Any, client: Any, file_api: Any
) -> Any:
    if result == "fails":
        with pytest.raises(OPException):
            check_if_item_id_in_items(path, client, file_api)
    else:
        check_if_item_id_in_items(path, client, file_api)


def create_directory_structure_in_op_rest(
    user: Any, users: Any, hosts: Any, host: Any, config: Any, space: Any, request: Any
) -> Any:
    items = yaml.load(config, yaml.Loader)
    cwd = space
    create_content(
        user, users, cwd, items, create_item_in_op_rest, host, hosts, request
    )


def create_item_in_op_rest(
    user: Any,
    users: Any,
    cwd: Any,
    name: Any,
    content: Any,
    create_item_fun: Any,
    host: Any,
    hosts: Any,
    request: Any,
) -> Any:
    if name.startswith("dir"):
        create_dir_in_op_rest(user, users, host, hosts, f"{cwd}/{name}", "")
    else:
        create_file_in_op_rest(user, users, host, hosts, f"{cwd}/{name}", "")
    if not content:
        return
    cwd += "/" + name
    create_content(user, users, cwd, content, create_item_fun, host, hosts, request)


def assert_ace_in_op_rest(
    user: Any,
    users: Any,
    host: Any,
    hosts: Any,
    numerals: Any,
    path: Any,
    num: Any,
    priv: Any,
    item_type: Any,
    name: Any,
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    ace = client.read_metadata(path)["metadata"]["cdmi_acl"][numerals[num]]
    assert_ace(priv, item_type, ace, name, num, path)


def grant_acl_privileges_in_op_rest(
    user: Any,
    users: Any,
    host: Any,
    hosts: Any,
    path: Any,
    priv: Any,
    item_type: Any,
    name: Any,
    groups: Any,
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    try:
        acl = client.read_metadata(path)["metadata"]["cdmi_acl"]
    except KeyError:
        acl = []
    acl = get_acl_metadata(acl, priv, item_type, groups, name, users, path)
    client.write_metadata(path, {"cdmi_acl": acl})


def write_to_file_in_op_rest(
    user: Any, users: Any, host: Any, hosts: Any, path: Any, text: Any, offset: Any = 0
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    client.write_to_file(path, text, offset)


def append_to_file_in_op_rest(
    user: Any, users: Any, host: Any, hosts: Any, path: Any, text: Any
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    metadata = client.read_metadata(path)["metadata"]
    try:
        file_size = int(metadata["cdmi_size"])
    except KeyError:
        assert False, f"File {path} has no size metadata"
    else:
        client.write_to_file(path, text, file_size)


def move_item_in_op_rest(
    src_path: Any,
    dst_path: Any,
    result: Any,
    host: Any,
    hosts: Any,
    user: Any,
    users: Any,
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    if result == "fails":
        with pytest.raises(HTTPError):
            client.move_item(src_path, dst_path)
    else:
        client.move_item(src_path, dst_path)


def move_item_in_op_rest_using_token(
    src_path: Any,
    dst_path: Any,
    result: Any,
    host: Any,
    hosts: Any,
    user: Any,
    tmp_memory: Any,
) -> Any:
    access_token = tmp_memory[user]["mailbox"].get("token", None)
    client = cdmi(hosts[host]["hostname"], access_token)
    if result == "fails":
        with pytest.raises(HTTPError):
            client.move_item(src_path, dst_path)
    else:
        client.move_item(src_path, dst_path)


def copy_item_in_op_rest(
    src_path: Any, dst_path: Any, host: Any, hosts: Any, user: Any, users: Any
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    client.copy_item(src_path, dst_path)


def assert_posix_permissions_in_op_rest(
    path: Any, perms: Any, user: Any, users: Any, host: Any, hosts: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    file_id = _lookup_file_id(path, user_client_op)
    file_attrs = file_api.get_attrs(file_id, data={"attributes": ["posix_permissions"]})
    try:
        file_perms = int(file_attrs.posix_permissions) % 1000
    except KeyError:
        assert False, f"File {path} has no mode metadata"

    assert file_perms == int(
        perms
    ), f"Expected file POSIX permissions for {path} to be {perms} but got {file_perms}"


def set_posix_permissions_in_op_rest(
    path: Any, perm: Any, user: Any, users: Any, host: Any, hosts: Any, result: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    file_id = _lookup_file_id(path, user_client_op)

    if result == "fails":
        with pytest.raises(OPException):
            file_api.set_attr(file_id, attribute={"mode": perm})
    else:
        file_api.set_attr(file_id, attribute={"mode": perm})


def get_time_for_file_in_op_rest(
    path: Any, user: Any, users: Any, host: Any, hosts: Any, time_name: Any
) -> Any:
    client = cdmi(hosts[host]["hostname"], users[user].token)
    metadata = client.read_metadata(path)["metadata"]
    attr = time_attr(time_name, "cdmi")
    date_fmt = "%Y-%m-%dT%H:%M:%SZ"

    try:
        time = datetime.strptime(metadata[attr], date_fmt)
    except KeyError as ex:
        raise AssertionError(f"File {path} has no {ex.args[0]} metadata") from ex

    return time


def compare_file_time_with_copied_time_in_op_rest(
    path: Any,
    user: Any,
    users: Any,
    host: Any,
    hosts: Any,
    time_name1: Any,
    time2: Any,
    comparator: Any,
    time_name2: Any,
) -> Any:
    time1 = get_time_for_file_in_op_rest(path, user, users, host, hosts, time_name1)
    err_msg = (
        f"Time comparison failed. \nTime1: {time_name1} = {time1} \n"
        f"Time2: {time_name2} = {time2} \nComparator: {comparator}"
    )
    assert compare(time1, time2, comparator), err_msg


def assert_files_time_relation_in_op_rest(
    path: Any,
    path2: Any,
    time1_name: Any,
    time2_name: Any,
    comparator: Any,
    host: Any,
    hosts: Any,
    user: Any,
    users: Any,
) -> Any:
    time1 = get_time_for_file_in_op_rest(path, user, users, host, hosts, time1_name)
    time2 = get_time_for_file_in_op_rest(path2, user, users, host, hosts, time2_name)

    err_msg = (
        f"Time comparison failed. \nTime1: {time1_name} = {time1} \n"
        f"Time2: {time2_name} = {time2} \nComparator: {comparator}"
    )

    assert compare(time1, time2, comparator), err_msg


def assert_time_relation_in_op_rest(
    path: Any,
    time1_name: Any,
    time2_name: Any,
    comparator: Any,
    host: Any,
    hosts: Any,
    user: Any,
    users: Any,
) -> Any:
    assert_files_time_relation_in_op_rest(
        path,
        path,
        time1_name,
        time2_name,
        comparator,
        host,
        hosts,
        user,
        users,
    )


def upload_file_rest(
    users: Any,
    user: Any,
    hosts: Any,
    host: Any,
    path: Any,
    file_name: Any,
    parent_id: Any,
) -> Any:
    if path == "":
        data = None
    else:
        with open(path, "rb") as f:
            data = f.read()
    provider_hostname = hosts[host]["hostname"]
    # standard urllib2 cannot handle streaming bytes
    _ = http_post(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", parent_id, f"children?name={file_name}"),
        headers={
            "X-Auth-Token": users[user].token,
            "Content-Type": "application/octet-stream",
        },
        data=data,
    )


def get_space_details_rest(
    users: Any, user: Any, hosts: Any, host: Any, space_id: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    space_api = SpaceApi(user_client_op)
    space_details = space_api.get_space(space_id)
    return space_details


def get_share_details_rest(
    users: Any, user: Any, hosts: Any, host: Any, share_id: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    share_api = ShareApi(user_client_op)
    share_details = share_api.get_share(share_id)
    return share_details


def create_share_rest(
    users: Any, user: Any, hosts: Any, host: Any, file_id: Any, name: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    share_api = ShareApi(user_client_op)
    share_id = share_api.create_share(data={"name": name, "rootFileId": file_id})
    return share_id


def remove_file_by_id_rest(
    users: Any, user: Any, hosts: Any, host: Any, file_id: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    file_api.remove_file(file_id)


def create_empty_file_in_dir_rest(
    users: Any, user: Any, hosts: Any, host: Any, dir_id: Any, name: Any
) -> Any:
    upload_file_rest(users, user, hosts, host, "", name, dir_id)


def get_file_hardlinks_rest(
    users: Any, user: Any, hosts: Any, host: Any, file_id: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    list_hardlinks = file_api.get_file_hardlinks(file_id)
    return list_hardlinks


def get_file_symlink_value_rest(
    users: Any, user: Any, hosts: Any, host: Any, file_id: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    symlink_val = file_api.get_symlink_value(file_id)
    return symlink_val


def check_for_hardlink_between_files_rest(
    users: Any, user: Any, hosts: Any, host: Any, hardlink_id: Any, file_id: Any
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    try:
        file_api.test_for_hardlink_between_files(hardlink_id, file_id)
        return True
    except OPException as e:
        if e.status != 404:
            raise e
        return False


def create_hardlink_rest(
    users: Any,
    user: Any,
    hosts: Any,
    host: Any,
    destination_dir_id: Any,
    target_id: Any,
    name: Any,
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    file_api.create_file(
        id=destination_dir_id,
        name=name,
        type="LNK",
        target_file_id=target_id,
        content="example",
    )
    # Providing non-empty content is necessary due to Swagger issues.
    # It is probably related to the fact that creating file with swaggers
    # sets: header_params['Content-Type'] = ['application/octet-stream'],
    # which only accepts non empty body.
    # Also the given content is ignored further by backend and in GUI we
    # can see the hardlink/symlink with empty content.


def create_symlink_rest(
    users: Any,
    user: Any,
    hosts: Any,
    host: Any,
    destination_dir_id: Any,
    target_path: Any,
    name: Any,
) -> Any:
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_api = BasicFileOperationsApi(user_client_op)
    file_api.create_file(
        id=destination_dir_id,
        name=name,
        type="SYMLNK",
        target_file_path=target_path,
        content="example",
    )
    # Providing content parameter for the same reason as in the function above
