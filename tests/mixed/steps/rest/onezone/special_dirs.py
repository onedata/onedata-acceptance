"""This module contains gherkin steps to run acceptance tests featuring
basic operations on special dirs in Onezone using REST API, oneclient.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Mapping
from typing import Optional, cast

from oneprovider_client.rest import ApiException

from tests.gui.utils import CDMIClient as cdmi
from tests.gui.utils.generic import SpecialDir
from tests.mixed.steps.oneclient.data_basic import change_client_name_to_hostname
from tests.mixed.steps.rest.oneprovider.data import (
    create_empty_file_in_dir_rest,
    create_share_rest,
    get_share_details_rest,
    get_space_details_rest,
    remove_file_by_id_rest,
)
from tests.mixed.steps.rest.oneprovider.datasets import create_dataset_in_op_by_id_rest
from tests.mixed.steps.rest.oneprovider.metadata import add_json_metadata_to_file_rest
from tests.mixed.steps.rest.oneprovider.qos import (
    create_qos_requirement_in_op_by_id_rest,
)
from tests.mixed.types import (
    HostsConfig,
    SpecialDirsTmpMemory as TmpMemory,
    Spaces,
    UsersWithToken as UserTokenMap,
)
from tests.mixed.type_definitions import SpecialDirsTmpMemory as TmpMemory
from tests.mixed.utils.common import NoSuchClientException
from tests.oneclient.steps.multi_dir_steps import (
    delete_dir_by_id,
    move_dir_by_id,
    try_to_delete_root_dir,
    try_to_move_root_dir,
)
from tests.oneclient.steps.multi_file_steps import (
    create_file_in_dir_by_id,
    try_to_create_file_in_root_dir,
)
from tests.types import Hosts, Users
from tests.utils.bdd_utils import parsers, wt
from tests.utils.http_exceptions import HTTPBadRequest

EX_ERR_MSGS_REST = [
    "Operation failed with POSIX error: enotsup.",
    "This operation is not supported.",
]

EX_ERR_MSG_OC = "Operation not supported"


def get_space_dir_id(
    users: Users,
    user: str,
    hosts: Hosts,
    host: str,
    space_name: str,
    spaces: Spaces,
    tmp_memory: TmpMemory,
) -> None:
    space_details = get_space_details_rest(users, user, hosts, host, spaces[space_name])
    if tmp_memory[SpecialDir.SPACE_DIR]:
        tmp_memory[SpecialDir.SPACE_DIR][space_name] = space_details.dir_id
    else:
        tmp_memory[SpecialDir.SPACE_DIR] = {space_name: space_details.dir_id}


@wt(
    parsers.parse(
        "using REST, {user} gets ID of the space archives directory "
        'from the space "{space_name}" details in {host}'
    )
)
def get_space_archives_dir_id(
    users: Users,
    user: str,
    hosts: Hosts,
    host: str,
    space_name: str,
    spaces: Spaces,
    tmp_memory: TmpMemory,
) -> None:
    space_details = get_space_details_rest(users, user, hosts, host, spaces[space_name])
    if tmp_memory[SpecialDir.SPACE_ARCHIVES_DIR]:
        tmp_memory[SpecialDir.SPACE_ARCHIVES_DIR][user] = space_details.archives_dir_id
    else:
        tmp_memory[SpecialDir.SPACE_ARCHIVES_DIR] = {
            user: space_details.archives_dir_id
        }


@wt(
    parsers.parse(
        "using REST, {user} gets ID of the trash directory from "
        'the space "{space_name}" details in {host}'
    )
)
def get_trash_dir_id(
    users: Users,
    user: str,
    hosts: Hosts,
    host: str,
    space_name: str,
    spaces: Spaces,
    tmp_memory: TmpMemory,
) -> None:
    space_details = get_space_details_rest(users, user, hosts, host, spaces[space_name])
    if tmp_memory[SpecialDir.TRASH_DIR]:
        tmp_memory[SpecialDir.TRASH_DIR][user] = space_details.trash_dir_id
    else:
        tmp_memory[SpecialDir.TRASH_DIR] = {user: space_details.trash_dir_id}


@wt(
    parsers.parse(
        "using REST, {user} gets ID of the share container from "
        'the share details in the space "{space_name}" in {host}'
    )
)
def get_share_container_id(
    users: Users,
    user: str,
    hosts: Hosts,
    host: str,
    space_name: str,
    spaces: Spaces,
    tmp_memory: TmpMemory,
) -> None:
    get_space_dir_id(users, user, hosts, host, space_name, spaces, tmp_memory)
    share_id = create_share_rest(
        users,
        user,
        hosts,
        host,
        tmp_memory[SpecialDir.SPACE_DIR][space_name],
        "test_share",
    ).share_id
    share_details = get_share_details_rest(users, user, hosts, host, share_id)
    if tmp_memory[SpecialDir.SHARE_CONTAINER]:
        tmp_memory[SpecialDir.SHARE_CONTAINER][user] = share_details.root_file_id
    else:
        tmp_memory[SpecialDir.SHARE_CONTAINER] = {user: share_details.root_file_id}


def _assert_ex_err_msg_rest(err_msg: str) -> None:
    assert any(
        ex in err_msg for ex in EX_ERR_MSGS_REST
    ), f"Unexpected error occurred:\n {err_msg}"


def _assert_ex_err_msg_oc(err_msg: str) -> None:
    assert EX_ERR_MSG_OC in err_msg, f"Unexpected error occurred:\n {err_msg}"


@wt(
    parsers.parse(
        "using {client}, {user} fails to remove the {name:SpecialDir} in {host}",
        extra_types={"SpecialDir": SpecialDir},
    )
)
def try_to_remove_special_dir(
    client: str,
    users: Users,
    user: str,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    name: SpecialDir,
) -> None:
    try_to_remove_special_dir_by_id(
        client,
        users,
        user,
        hosts,
        host,
        tmp_memory[name][user],
        err_msg=f"{name.value} was deleted!",
    )


def try_to_remove_special_dir_by_id(
    client: str,
    users: Users,
    user: str,
    hosts: Hosts,
    host: str,
    dir_id: str,
    err_msg: str = "",
) -> None:
    if client.lower() == "rest":
        try:
            remove_file_by_id_rest(users, user, hosts, host, dir_id)
            raise AssertionError(err_msg)
        except ApiException as e:
            _assert_ex_err_msg_rest(str(e))
    elif "oneclient" in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            delete_dir_by_id(user, oneclient_host, users, dir_id)
            raise AssertionError(err_msg)
        except OSError as e:
            _assert_ex_err_msg_oc(str(e))
    else:
        raise NoSuchClientException(f"unknown client {client}")


@wt(
    parsers.parse(
        "using {client}, {user} fails to remove the user root "
        "directory using file path in {host}"
    )
)
def try_to_remove_user_root_dir_by_path(client: str, users: Users, user: str) -> None:
    if "oneclient" in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            try_to_delete_root_dir(user, oneclient_host, users)
            raise AssertionError("Space root dir was deleted!")
        except OSError as e:
            _assert_ex_err_msg_oc(str(e))
    else:
        raise NoSuchClientException(f"unknown client {client}")


@wt(
    parsers.parse(
        "using {client}, {user} fails to move the {name:SpecialDir} in {host}",
        extra_types={"SpecialDir": SpecialDir},
    )
)
def try_to_move_special_dir(
    client: str,
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    name: SpecialDir,
) -> None:
    try_to_move_special_dir_by_id(
        client,
        user,
        users,
        hosts,
        host,
        tmp_memory[name][user],
        err_msg=f"Moved {name.value}, but moving should have failed",
    )


def try_to_move_special_dir_by_id(
    client: str,
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    dir_id: str,
    err_msg: Optional[str] = None,
) -> None:
    if client.lower() == "rest":
        try:
            cdmi_client = cdmi(hosts[host]["ip"], users[user].token)
            cdmi_client.move_item_by_id(dir_id, "/new_name")
            raise AssertionError(err_msg)
        except HTTPBadRequest as e:
            assert "Operation failed with POSIX error: enoent." in str(
                e
            ), f"Unexpected error occurred:\n {e}"
    elif "oneclient" in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            move_dir_by_id(user, oneclient_host, users, dir_id, "new_name")
            raise AssertionError(err_msg)
        except OSError as e:
            # Because the share container id is very long other error can occur
            assert "Operation not supported" in str(e) or "File name too long" in str(
                e
            ), f"Unexpected error occurred:\n {e}"
    else:
        raise NoSuchClientException(f"unknown client {client}")


@wt(
    parsers.parse(
        "using {client}, {user} fails to move the "
        "user root directory using file path in {host}"
    )
)
def try_to_move_user_root_dir_by_path(client: str, user: str, users: Users) -> None:
    if "oneclient" in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            try_to_move_root_dir(user, oneclient_host, users, "new_name")
            raise AssertionError("moved user root dir, but moving should have failed")
        except OSError as e:
            _assert_ex_err_msg_oc(str(e))
    else:
        raise NoSuchClientException(f"unknown client {client}")


@wt(
    parsers.parse(
        'using {client}, {user} fails to create file "{file_name}" '
        "in the {name:SpecialDir} in {host}",
        extra_types={"SpecialDir": SpecialDir},
    )
)
def try_to_create_file_in_special_dir(
    client: str,
    users: Users,
    user: str,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    file_name: str,
    name: SpecialDir,
) -> None:
    try_to_create_file_in_special_dir_by_id(
        client,
        users,
        user,
        hosts,
        host,
        tmp_memory[name][user],
        file_name,
        err_msg=f"File created in {name.value}, but creation should have failed",
    )


def try_to_create_file_in_special_dir_by_id(
    client: str,
    users: Users,
    user: str,
    hosts: Hosts,
    host: str,
    dir_id: str,
    file_name: str,
    err_msg: str = "",
) -> None:
    if client.lower() == "rest":
        try:
            create_empty_file_in_dir_rest(users, user, hosts, host, dir_id, file_name)
            raise AssertionError(err_msg)
        except HTTPBadRequest as e:
            _assert_ex_err_msg_rest(str(e))
    elif "oneclient" in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            create_file_in_dir_by_id(user, oneclient_host, users, dir_id, file_name)
            raise AssertionError(err_msg)
        except OSError as e:
            _assert_ex_err_msg_oc(str(e))


@wt(
    parsers.parse(
        'using {client}, {user} fails to create file "{file_name}" '
        "in the user root directory using file path in {host}"
    )
)
def try_to_create_file_in_user_root_dir_by_path(
    client: str, users: Users, user: str, file_name: str
) -> None:
    if "oneclient" in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            try_to_create_file_in_root_dir(user, oneclient_host, users, file_name)
            raise AssertionError(
                "file created in user root dir, but creation should have failed"
            )
        except OSError as e:
            _assert_ex_err_msg_oc(str(e))


@wt(
    parsers.parse(
        "using REST, {user} fails to add QoS requirement "
        '"{expression}" to the {name:SpecialDir} in {host}',
        extra_types={"SpecialDir": SpecialDir},
    )
)
def try_to_add_qos_to_special_dir(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    expression: str,
    name: SpecialDir,
) -> None:
    try_to_add_qos_to_special_dir_by_id(
        user,
        users,
        hosts,
        host,
        tmp_memory[name][user],
        expression,
        err_msg=f"Qos requirement added to {name.value}, but adding should have failed",
    )


def try_to_add_qos_to_special_dir_by_id(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    dir_id: str,
    expression: str,
    err_msg: str = "",
) -> None:
    try:
        create_qos_requirement_in_op_by_id_rest(
            user,
            users,
            cast(HostsConfig, hosts),
            host,
            expression,
            dir_id,
        )
        raise AssertionError(err_msg)
    except ApiException as e:
        _assert_ex_err_msg_rest(str(e))


@wt(
    parsers.parse(
        "using REST, {user} fails to add json metadata "
        "'{expression}' to the {name:SpecialDir} in {host}",
        extra_types={"SpecialDir": SpecialDir},
    )
)
def try_to_add_json_metadata_to_special_dir(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    expression: str,
    name: SpecialDir,
) -> None:
    try_to_add_json_metadata_to_special_dir_by_id(
        user,
        users,
        hosts,
        host,
        tmp_memory[name][user],
        expression,
        err_msg=f"Json metadata added to {name.value}, but adding should have failed",
    )


def try_to_add_json_metadata_to_special_dir_by_id(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    dir_id: str,
    expression: str,
    err_msg: str = "",
) -> None:
    try:
        add_json_metadata_to_file_rest(
            user,
            users,
            cast(HostsConfig, hosts),
            host,
            expression,
            dir_id,
        )
        raise AssertionError(err_msg)
    except ApiException as e:
        _assert_ex_err_msg_rest(str(e))


@wt(
    parsers.parse(
        "using REST, {user} fails to establish dataset on the {name:SpecialDir} in"
        " {host}",
        extra_types={"SpecialDir": SpecialDir},
    )
)
def try_to_establish_dataset_on_special_dir(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    name: SpecialDir,
) -> None:
    try_to_establish_dataset_on_special_dir_by_id(
        user,
        users,
        hosts,
        host,
        tmp_memory[name][user],
        err_msg=(
            f"Established dataset on {name.value}, but establishing should have failed"
        ),
    )


def try_to_establish_dataset_on_special_dir_by_id(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    dir_id: str,
    err_msg: str = "",
) -> None:
    try:
        create_dataset_in_op_by_id_rest(user, users, hosts, host, dir_id, "")
        raise AssertionError(err_msg)
    except ApiException as e:
        _assert_ex_err_msg_rest(str(e))
