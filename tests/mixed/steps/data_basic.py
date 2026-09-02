"""This module contains gherkin steps to run mixed acceptance tests featuring
basic operations on data using web GUI and REST.
"""

__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import re
from collections.abc import Mapping
from typing import Optional, cast

import pytest
from _pytest._py.path import LocalPath

from tests.gui.constants import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.data import (
    assert_file_content_in_op_gui,
    assert_mtime_not_earlier_than_op_gui,
    assert_space_content_in_op_gui,
    change_cwd_using_breadcrumbs_in_data_tab_in_op,
    check_file_owner,
    create_directory_structure_in_op_gui,
    create_item_in_op_gui,
    go_to_filebrowser,
    go_to_path_without_last_elem,
    remove_dir_and_parents_in_op_gui,
    remove_item_in_op_gui,
    rename_item,
    see_items_in_op_gui,
    see_num_of_items_in_path_in_op_gui,
    successfully_upload_file_to_op_gui,
)
from tests.gui.meta_steps.oneprovider.metadata import (
    assert_metadata_in_op_gui,
    assert_such_metadata_not_exist_in_op_gui,
    remove_all_metadata_in_op_gui,
    set_metadata_in_op_gui,
)
from tests.gui.steps.oneprovider.browser import click_and_press_enter_on_item_in_browser
from tests.gui.steps.oneprovider.data_tab import upload_file_to_cwd_in_data_tab
from tests.gui.type_definitions import TmpMemory
from tests.mixed.steps.oneclient.data_basic import (
    assert_metadata_in_op_oneclient,
    assert_no_such_metadata_in_op_oneclient,
    assert_num_of_files_in_path_in_op_oneclient,
    assert_space_content_in_op_oneclient,
    change_client_name_to_hostname,
    compare_file_time_with_copied_time_in_op_oneclient,
    copy_item_in_op_oneclient,
    create_dir_in_op_oneclient,
    create_directory_structure_in_op_oneclient,
    create_file_in_op_oneclient,
    create_file_in_op_oneclient_with_tokens,
    delete_empty_directory_in_op_oneclient,
    get_time_for_file_in_op_oneclient,
    move_item_in_op_oneclient,
    multi_dir_steps,
    multi_file_steps,
    multi_reg_file_steps,
    remove_all_metadata_in_op_oneclient,
    remove_file_in_op_oneclient,
    see_items_in_op_oneclient,
    set_metadata_in_op_oneclient,
)
from tests.mixed.steps.rest.oneprovider.data import (
    append_to_file_in_op_rest,
    assert_file_content_in_op_rest,
    assert_files_time_relation_in_op_rest,
    assert_num_of_files_in_path_in_op_rest,
    assert_space_content_in_op_rest,
    assert_time_relation_in_op_rest,
    compare_file_time_with_copied_time_in_op_rest,
    copy_item_in_op_rest,
    create_dir_in_op_rest,
    create_directory_structure_in_op_rest,
    create_file_in_op_rest,
    get_time_for_file_in_op_rest,
    move_item_in_op_rest,
    move_item_in_op_rest_using_token,
    remove_dir_in_op_rest,
    remove_file_in_op_rest,
    remove_file_using_token_in_op_rest,
    see_item_in_op_rest_using_token,
    see_items_in_op_rest,
    write_to_file_in_op_rest,
)
from tests.mixed.steps.rest.oneprovider.metadata import (
    HostsConfig as MetadataHostsConfig,
)
from tests.mixed.steps.rest.oneprovider.metadata import (
    assert_metadata_in_op_rest,
    assert_no_such_metadata_in_op_rest,
    remove_all_metadata_in_op_rest,
    set_metadata_in_op_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.type_definitions import EnvDesc, Hosts, SeleniumDrivers, Tokens
from tests.utils.bdd_utils import parsers, wt
from tests.utils.http_exceptions import HTTPBadRequest
from tests.utils.path_utils import get_first_path_element
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


def _as_metadata_users(users: Users) -> Users:
    return users


def _as_metadata_hosts(hosts: Hosts) -> MetadataHostsConfig:
    return cast(MetadataHostsConfig, hosts)


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create "
        r'file named "(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def create_file_in_op(
    client: str,
    user: str,
    users: Users,
    space: str,
    name: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    host: str,
    selenium: SeleniumDrivers,
    result: str,
    request: pytest.FixtureRequest,
) -> None:
    full_path = f"{space}/{name}"
    client_lower = client.lower()
    if client_lower == "web gui":
        create_item_in_op_gui(
            selenium,
            user,
            os.path.dirname(name),
            "file",
            os.path.basename(name),
            tmp_memory,
            result,
            space,
        )
    elif client_lower == "rest":
        create_file_in_op_rest(user, users, host, hosts, full_path, result)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        create_file_in_op_oneclient(
            user, full_path, users, result, oneclient_host, request
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>\w+\s?\w*), (?P<user>\w+) (?P<result>\w+) "
        r'to create file named "(?P<name>.*)" using received token in '
        r'"(?P<space>.*)" in (?P<host>.*)'
    )
)
def create_file_in_op_with_token(
    client: str,
    user: str,
    users: Users,
    space: str,
    name: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    host: str,
    result: str,
    env_desc: EnvDesc,
    request: pytest.FixtureRequest,
) -> None:
    full_path = f"{space}/{name}"
    client_lower = client.lower()
    if client_lower == "rest":
        token = tmp_memory[user]["mailbox"].get("token", None)
        create_file_in_op_rest(user, users, host, hosts, full_path, result, token)
    elif "oneclient" in client_lower:
        create_file_in_op_oneclient_with_tokens(
            user,
            hosts,
            users,
            env_desc,
            tmp_memory,
            result,
            full_path,
            client_lower,
            request,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to see "
        r'item named "(?P<name>[^ ]+)" using received access token in '
        r'"(?P<space>.*)" in (?P<host>.*)'
    )
)
def assert_file_in_op_with_token(
    client: str,
    user: str,
    name: str,
    space: str,
    host: str,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    result: str,
) -> None:

    client_lower = client.lower()
    if client_lower == "rest":
        see_item_in_op_rest_using_token(
            user, name, space, host, tmp_memory, users, hosts, result
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        see_items_in_op_oneclient([name], space, user, users, result, oneclient_host)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*) with identity token, (?P<user>\w+) ("
        r'?P<result>\w+) to create file named "(?P<name>.*)" using '
        r'received token in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def create_file_in_op_with_tokens(
    client: str,
    user: str,
    users: Users,
    space: str,
    name: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    host: str,
    result: str,
    env_desc: EnvDesc,
    tokens: Tokens,
    request: pytest.FixtureRequest,
) -> None:
    full_path = f"{space}/{name}"
    client_lower = client.lower()
    if client_lower == "rest":
        access_token = tmp_memory[user]["mailbox"].get("token", None)
        identity_token = tokens[f"identity_token_of_{user}"].get("token", None)
        create_file_in_op_rest(
            user,
            users,
            host,
            hosts,
            full_path,
            result,
            access_token=access_token,
            identity_token=identity_token,
        )
    elif "oneclient" in client_lower:
        create_file_in_op_oneclient_with_tokens(
            user,
            hosts,
            users,
            env_desc,
            tmp_memory,
            result,
            full_path,
            client_lower,
            request,
        )

    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create "
        r'directory named "/(?P<abs_path>.*)" in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def create_dir_in_op(
    client: str,
    user: str,
    users: Users,
    space: str,
    abs_path: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    host: str,
    selenium: SeleniumDrivers,
    result: str,
) -> None:
    cwd = "space root"
    full_path = f"{space}/{abs_path}"
    client_lower = client.lower()
    if client_lower == "web gui":
        if "/" in abs_path:
            go_to_filebrowser(selenium, user, tmp_memory, space)
            go_to_path_without_last_elem(selenium, user, tmp_memory, abs_path)
            create_item_in_op_gui(
                selenium,
                user,
                "",
                "directory",
                os.path.basename(abs_path),
                tmp_memory,
                result,
                space,
            )
            change_cwd_using_breadcrumbs_in_data_tab_in_op(selenium, user, cwd)
        else:
            create_item_in_op_gui(
                selenium,
                user,
                os.path.dirname(abs_path),
                "directory",
                os.path.basename(abs_path),
                tmp_memory,
                result,
                space,
            )
    elif client_lower == "rest":
        create_dir_in_op_rest(user, users, host, hosts, full_path, result)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        create_dir_in_op_oneclient(user, full_path, users, result, oneclient_host)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using web GUI, (?P<user>\w+) clicks and presses enter on item "
        r'named "(?P<item_name>.*)" in "(?P<space>.*)"'
    )
)
def go_to_dir(
    selenium: SeleniumDrivers,
    user: str,
    item_name: str,
    tmp_memory: TmpMemory,
    space: str,
) -> None:
    go_to_filebrowser(selenium, user, tmp_memory, space)
    click_and_press_enter_on_item_in_browser(
        selenium, user, item_name, tmp_memory, "file browser"
    )


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to see "
        r'item named "(?P<name>[^ ]+)" in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def see_item_in_op(
    client: str,
    user: str,
    users: Users,
    result: str,
    name: str,
    space: str,
    host: str,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        name_list = name
        path = ""
        if "/" in name_list:
            name = name_list.split("/")[-1]
            path = name_list.replace(name, "")[:-1]

        see_items_in_op_gui(
            selenium,
            user,
            path,
            [name],
            tmp_memory,
            result,
            space,
        )
    elif client_lower == "rest":
        see_items_in_op_rest(user, users, host, hosts, [name], result, space)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        see_items_in_op_oneclient([name], space, user, users, result, oneclient_host)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to "
        r'remove directory \(rmdir\) named "(?P<name>.*)" in '
        r'"(?P<space>.*)" in (?P<host>.*)'
    )
)
def remove_empty_dir_in_op(
    client: str,
    user: str,
    users: Users,
    result: str,
    space: str,
    name: str,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    host: str,
) -> None:
    full_path = f"{space}/{name}"
    client_lower = client.lower()
    if client_lower == "web gui":
        remove_item_in_op_gui(
            selenium,
            user,
            name,
            tmp_memory,
            "succeds",
            space,
        )
    elif client_lower == "rest":
        remove_dir_in_op_rest(user, users, host, hosts, full_path)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        delete_empty_directory_in_op_oneclient(
            full_path, user, users, result, oneclient_host
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) removes directory "
        r'\(rmdir -p\) named "(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def remove_empty_dir_and_parents_in_op(
    client: str,
    user: str,
    users: Users,
    space: str,
    name: str,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    host: str,
) -> None:
    first_path_elem = get_first_path_element(name)
    client_lower = client.lower()
    if client_lower == "web gui":
        remove_dir_and_parents_in_op_gui(
            selenium,
            user,
            first_path_elem,
            tmp_memory,
            "succeds",
            space,
        )
    elif client_lower == "rest":
        remove_dir_in_op_rest(user, users, host, hosts, f"{space}/{first_path_elem}")
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_dir_steps.delete_parents(user, f"{space}/{name}", oneclient_host, users)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) removes directory "
        r'\(rm -rf\) named "(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def remove_dir_in_op(
    client: str,
    user: str,
    users: Users,
    space: str,
    name: str,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    host: str,
) -> None:
    full_path = f"{space}/{name}"
    client_lower = client.lower()
    if client_lower == "web gui":
        remove_item_in_op_gui(
            selenium,
            user,
            name,
            tmp_memory,
            "succeds",
            space,
        )
    elif client_lower == "rest":
        remove_dir_in_op_rest(user, users, host, hosts, full_path)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_dir_steps.delete_non_empty(user, full_path, oneclient_host, users)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) "
        r'to remove file named "(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def remove_file_in_op(
    client: str,
    user: str,
    name: str,
    space: str,
    host: str,
    users: Users,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    result: str,
) -> None:
    full_path = f"{space}/{name}"
    client_lower = client.lower()
    if client_lower == "web gui":
        remove_item_in_op_gui(
            selenium,
            user,
            name,
            tmp_memory,
            result,
            space,
        )
    elif client_lower == "rest":
        remove_file_in_op_rest(user, users, host, hosts, full_path, result)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        remove_file_in_op_oneclient(user, full_path, oneclient_host, users, result)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) "
        r'to remove file named "(?P<name>.*)" using received token in '
        r'"(?P<space>.*)" in (?P<host>.*)'
    )
)
def remove_file_using_token_in_op(
    client: str,
    user: str,
    name: str,
    space: str,
    host: str,
    users: Users,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    result: str,
) -> None:
    full_path = f"{space}/{name}"
    client_lower = client.lower()
    if client_lower == "rest":
        remove_file_using_token_in_op_rest(
            user, users, host, hosts, full_path, result, tmp_memory
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        remove_file_in_op_oneclient(user, full_path, oneclient_host, users, result)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) "
        r'renames item named "(?P<old_name>.*)" to "(?P<new_name>.*)" '
        r'in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def rename_item_in_op(
    client: str,
    user: str,
    users: Users,
    space: str,
    old_name: str,
    new_name: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    host: str,
    selenium: SeleniumDrivers,
) -> None:
    old_path = f"{space}/{old_name}"
    new_path = f"{space}/{new_name}"
    client_lower = client.lower()
    result = "succeeds"
    if client_lower == "web gui":
        rename_item(
            selenium,
            user,
            old_name,
            new_name,
            tmp_memory,
            result,
            space,
        )
    elif client_lower == "rest":
        move_item_in_op_rest(old_path, new_path, result, host, hosts, user, users)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.rename(user, old_path, new_path, oneclient_host, users)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) "
        r'renames item named "(?P<old_name>.*)" to "(?P<new_name>.*)" '
        r'using received access token in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def rename_item_in_op_using_token(
    client: str,
    user: str,
    users: Users,
    space: str,
    old_name: str,
    new_name: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    host: str,
) -> None:
    old_path = f"{space}/{old_name}"
    new_path = f"{space}/{new_name}"
    client_lower = client.lower()

    if client_lower == "rest":
        result = "succeds"
        move_item_in_op_rest_using_token(
            old_path,
            new_path,
            result,
            host,
            hosts,
            user,
            tmp_memory,
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.rename(user, old_path, new_path, oneclient_host, users)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that there "
        r'(is 1|are (?P<num>\d+)) items? in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def see_num_of_items_in_op(
    client: str,
    user: str,
    num: Optional[str],
    space: str,
    host: str,
    users: Users,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
) -> None:
    num_value = int(num) if num is not None else 1
    client_lower = client.lower()
    if client_lower == "web gui":
        see_num_of_items_in_path_in_op_gui(
            selenium,
            user,
            tmp_memory,
            "",
            num_value,
            host,
            hosts,
        )
    elif client_lower == "rest":
        assert_num_of_files_in_path_in_op_rest(
            num_value, space, user, users, host, hosts
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_num_of_files_in_path_in_op_oneclient(
            num_value, space, user, users, oneclient_host
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r'using (?P<client>.*), (?P<user>\w+) writes "(?P<text>.*)" '
        r'to file named "(?P<file_name>.*)" in '
        r'"(?P<space>.*)" in (?P<host>.*)'
    )
)
def write_to_file_in_op(
    client: str,
    user: str,
    text: str,
    file_name: str,
    space: str,
    host: str,
    users: Users,
    hosts: Hosts,
) -> None:
    full_path = f"{space}/{file_name}"
    client_lower = client.lower()
    if client_lower == "rest":
        write_to_file_in_op_rest(user, users, host, hosts, full_path, text)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_reg_file_steps.write_text(user, text, full_path, oneclient_host, users)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r'using (?P<client>.*), (?P<user>\w+) reads "(?P<text>.*)" '
        r'from file named "(?P<file_name>.*)" in '
        r'"(?P<space>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def read_from_file_in_op(
    client: str,
    user: str,
    text: str,
    file_name: str,
    space: str,
    host: str,
    users: Users,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    tmpdir: LocalPath,
) -> None:
    full_path = f"{space}/{file_name}"
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_file_content_in_op_gui(
            text,
            file_name,
            space,
            selenium,
            user,
            tmp_memory,
            tmpdir,
        )
    elif client_lower == "rest":
        assert_file_content_in_op_rest(full_path, text, user, users, host, hosts)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_reg_file_steps.read_text(user, text, full_path, oneclient_host, users)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>(succeeds|fails)) to append"
        r' "(?P<text>.*)" to file under a path "(?P<file_name>.*)" in '
        r'"(?P<space>.*)" in (?P<host>.*)'
    )
)
def append_to_file_in_op(
    client: str,
    user: str,
    result: str,
    text: str,
    file_name: str,
    space: str,
    host: str,
    users: Users,
    hosts: Hosts,
) -> None:
    full_path = f"{space}/{file_name}"
    client_lower = client.lower()
    if client_lower == "rest":
        if result == "succeeds":
            append_to_file_in_op_rest(user, users, host, hosts, full_path, text)
        else:
            try:
                append_to_file_in_op_rest(user, users, host, hosts, full_path, text)
                raise AssertionError("The append operation was supposed to fail")
            except (
                HTTPBadRequest
            ):  # If file is data write protected this exception will be thrown
                pass

    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        if result == "succeeds":
            multi_reg_file_steps.append(user, text, full_path, oneclient_host, users)
        else:
            raise NotImplementedError
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) replaces "
        r'"(?P<old_text>.*)" with "(?P<new_text>.*)" '
        r'in file named "(?P<file_name>.*)" in '
        r'"(?P<space>.*)" in (?P<host>.*)'
    )
)
def replace_in_file_in_op(
    client: str,
    user: str,
    old_text: str,
    new_text: str,
    file_name: str,
    space: str,
    users: Users,
) -> None:
    full_path = f"{space}/{file_name}"
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_reg_file_steps.replace(
            user, old_text, new_text, full_path, oneclient_host, users
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to move "
        r'"(?P<src_path>.*)" to "(?P<dst_path>.*)" in (?P<host>.*)'
    )
)
def move_file_in_op(
    client: str,
    user: str,
    result: str,
    src_path: str,
    dst_path: str,
    host: str,
    users: Users,
    hosts: Hosts,
) -> None:
    client_lower = client.lower()
    if client_lower == "rest":
        move_item_in_op_rest(src_path, dst_path, result, host, hosts, user, users)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        move_item_in_op_oneclient(
            user, src_path, dst_path, users, result, oneclient_host
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) copies "
        r"(?P<item_type>(directory|file)) named "
        r'"(?P<src_path>.*)" to "(?P<dst_path>.*)" in (?P<host>.*)'
    )
)
def copy_item_in_op(
    client: str,
    user: str,
    item_type: str,
    src_path: str,
    dst_path: str,
    host: str,
    users: Users,
    hosts: Hosts,
) -> None:
    client_lower = client.lower()
    if client_lower == "rest":
        copy_item_in_op_rest(src_path, dst_path, host, hosts, user, users)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        copy_item_in_op_oneclient(
            item_type, src_path, dst_path, user, users, oneclient_host
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) creates directory "
        r'structure in "(?P<space>.*)" space on (?P<host>.*) '
        r"as follow:\n(?P<config>(.|\s)*)"
    )
)
def create_directory_structure_in_op(
    selenium: SeleniumDrivers,
    user: str,
    config: str,
    space: str,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    host: str,
    client: str,
    request: pytest.FixtureRequest,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        create_directory_structure_in_op_gui(
            selenium,
            user,
            config,
            space,
            tmp_memory,
        )
    elif client_lower == "rest":
        create_directory_structure_in_op_rest(
            user, users, hosts, host, config, space, request
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        create_directory_structure_in_op_oneclient(
            user, users, config, space, oneclient_host, hosts, request
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")

    tmp_memory["config"] = config


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that (?P<time1>.*) "
        r'time of item named "(?P<file_name>.*)" in "(?P<space>.*)" '
        r"space is (?P<comparator>.*) "
        r"(?P<time2>.*) time in (?P<host>.*)"
    )
)
def assert_time_relation(
    user: str,
    time1: str,
    file_name: str,
    space: str,
    comparator: str,
    time2: str,
    client: str,
    users: Users,
    host: str,
    hosts: Hosts,
) -> None:
    client_lower = client.lower()
    full_path = f"{space}/{file_name}"
    comparator = re.sub(r"( than| to)", "", comparator)
    if client_lower == "rest":
        assert_time_relation_in_op_rest(
            full_path, time1, time2, comparator, host, hosts, user, users
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.check_time(
            user, time1, time2, comparator, full_path, oneclient_host, users
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) copies "
        r'(?P<time_name>.*) time of item named "(?P<file_name>.*)" in '
        r'"(?P<space>.*)" space in (?P<host>.*)'
    )
)
def remember_time_for_file(
    user: str,
    time_name: str,
    file_name: str,
    space: str,
    client: str,
    users: Users,
    host: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
) -> None:
    client_lower = client.lower()
    full_path = f"{space}/{file_name}"
    if client_lower == "rest":
        file_time = get_time_for_file_in_op_rest(
            full_path, user, users, host, hosts, time_name
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        file_time = get_time_for_file_in_op_oneclient(
            users, user, oneclient_host, time_name, full_path
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")

    tmp_memory[time_name] = file_time


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that "
        r'(?P<time_name1>.*) time of item named "(?P<file_name>.*)" '
        r'in space "(?P<space>.*)" is (?P<comparator>.*) (than|to) '
        r"(?P<time_name2>.*) time that was copied in (?P<host>.*)"
    )
)
def compare_file_time_with_copied_time(
    user: str,
    time_name1: str,
    time_name2: str,
    file_name: str,
    space: str,
    client: str,
    users: Users,
    host: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    comparator: str,
) -> None:
    client_lower = client.lower()
    full_path = f"{space}/{file_name}"
    time2 = tmp_memory[time_name1]
    if client_lower == "rest":
        compare_file_time_with_copied_time_in_op_rest(
            full_path,
            user,
            users,
            host,
            hosts,
            time_name1,
            time2,
            comparator,
            time_name2,
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        compare_file_time_with_copied_time_in_op_oneclient(
            users,
            user,
            oneclient_host,
            time_name1,
            full_path,
            time2,
            time_name2,
            comparator,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that (?P<time1>.*) "
        r'time of item named "(?P<file_name>.*)" is (?P<comparator>.*) '
        r"(than|to) (?P<time2>.*) time of item named "
        r'"(?P<file2_name>.*)" in "(?P<space>.*)" space in (?P<host>.*)'
    )
)
def assert_files_time_relation(
    user: str,
    time1: str,
    file_name: str,
    space: str,
    comparator: str,
    time2: str,
    client: str,
    file2_name: str,
    users: Users,
    host: str,
    hosts: Hosts,
) -> None:
    client_lower = client.lower()
    full_path = f"{space}/{file_name}"
    full_path2 = f"{space}/{file2_name}"
    if client_lower == "rest":
        assert_files_time_relation_in_op_rest(
            full_path,
            full_path2,
            time1,
            time2,
            comparator,
            host,
            hosts,
            user,
            users,
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.check_files_time(
            user,
            time1,
            time2,
            comparator,
            full_path,
            full_path2,
            oneclient_host,
            users,
        )
    else:
        raise NoSuchClientException(
            f"Client: {client} is not supported for this assertion"
        )


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.*) sees that "
        r'(?P<time_name>.*) time of item named "(?P<file_path>.*)" '
        r"in current space is not earlier than "
        r"(?P<time>[0-9]*) seconds ago in (?P<host>.*)"
    )
)
def assert_mtime_not_earlier_than(
    client: str,
    file_path: str,
    selenium: SeleniumDrivers,
    user: str,
    time: str,
    tmp_memory: TmpMemory,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_mtime_not_earlier_than_op_gui(
            file_path, time, user, tmp_memory, selenium
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that directory "
        r'structure in "(?P<space>.*)" space in (?P<host>.*) is as previously created'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_directory_structure_is_as_previous_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    tmp_memory: TmpMemory,
    tmpdir: LocalPath,
    space: str,
    host: str,
    spaces: Mapping[str, str],
    hosts: Hosts,
    users: Users,
) -> None:
    config = tmp_memory["config"]
    client_lower = client.lower()

    if client_lower == "web gui":
        assert_space_content_in_op_gui(
            config,
            selenium,
            user,
            tmp_memory,
            tmpdir,
            space,
        )
    elif client_lower == "rest":
        assert_space_content_in_op_rest(user, users, hosts, config, space, spaces, host)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_space_content_in_op_oneclient(config, space, user, users, oneclient_host)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that directory "
        r'structure in "(?P<space>.*)" space in (?P<host>.*) is as '
        r"follow:\n(?P<config>(.|\s)*)"
    )
)
def assert_directory_structure_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    tmp_memory: TmpMemory,
    tmpdir: LocalPath,
    space: str,
    host: str,
    spaces: Mapping[str, str],
    hosts: Hosts,
    users: Users,
    config: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_space_content_in_op_gui(
            config,
            selenium,
            user,
            tmp_memory,
            tmpdir,
            space,
        )
    elif client_lower == "rest":
        assert_space_content_in_op_rest(user, users, hosts, config, space, spaces, host)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_space_content_in_op_oneclient(config, space, user, users, oneclient_host)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sets new "
        r'(?P<tab_name>.*) metadata: (?P<val>.*) for "(?P<path>.*?)"'
        r' (?P<item>file|directory) in space "(?P<space>.*)" in (?P<host>.*)'
    )
)
def set_metadata_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    tab_name: str,
    val: str,
    space: str,
    path: str,
    host: str,
    hosts: Hosts,
    users: Users,
    tmp_memory: TmpMemory,
    item: str,
) -> None:
    full_path = f"{space}/{path}"
    client_lower = client.lower()
    if client_lower == "web gui":
        tab_name = tab_name.upper() if tab_name != "xattrs" else tab_name
        set_metadata_in_op_gui(
            selenium,
            user,
            path,
            tmp_memory,
            "s",
            space,
            tab_name,
            val,
            item,
        )
    elif client_lower == "rest":
        set_metadata_in_op_rest(
            user,
            _as_metadata_users(users),
            host,
            _as_metadata_hosts(hosts),
            full_path,
            tab_name,
            val,
        )
    elif "oneclient" in client_lower:
        if tab_name.lower() == "rdf":
            val = val.replace('"', '\\"')
            val = '"' + val + '"'
        oneclient_host = change_client_name_to_hostname(client_lower)
        set_metadata_in_op_oneclient(
            val, tab_name, full_path, user, users, oneclient_host
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that "
        r'(?P<tab_name>.*) metadata for "(?P<path>.*?)" '
        r"(?P<item>file|directory) is "
        r'(?P<val>.*) in space "(?P<space>.*)" in (?P<host>.*)'
    )
)
def assert_metadata_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    tab_name: str,
    val: str,
    space: str,
    path: str,
    host: str,
    hosts: Hosts,
    users: Users,
    tmp_memory: TmpMemory,
    item: str,
) -> None:
    full_path = f"{space}/{path}"
    client_lower = client.lower()
    if client_lower == "web gui":
        tab_name = tab_name.upper() if tab_name != "xattrs" else tab_name
        assert_metadata_in_op_gui(
            selenium,
            user,
            path,
            tmp_memory,
            "s",
            space,
            tab_name,
            val,
            item,
        )
    elif client_lower == "rest":
        assert_metadata_in_op_rest(
            user,
            _as_metadata_users(users),
            host,
            _as_metadata_hosts(hosts),
            full_path,
            tab_name,
            val,
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_metadata_in_op_oneclient(
            val, tab_name, full_path, user, users, oneclient_host
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) removes all "
        r'"(?P<path>.*)" (?P<item>file|directory) '
        r'metadata in space "(?P<space>\w+)" in (?P<host>.*)'
    )
)
def remove_all_metadata_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    users: Users,
    space: str,
    tmp_memory: TmpMemory,
    path: str,
    host: str,
    hosts: Hosts,
    item: str,
) -> None:
    full_path = f"{space}/{path}"
    client_lower = client.lower()
    if client_lower == "web gui":
        remove_all_metadata_in_op_gui(
            selenium,
            user,
            space,
            tmp_memory,
            path,
            item,
        )
    elif client_lower == "rest":
        remove_all_metadata_in_op_rest(
            user, _as_metadata_users(users), host, _as_metadata_hosts(hosts), full_path
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        remove_all_metadata_in_op_oneclient(user, users, oneclient_host, full_path)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that "
        r'(?P<tab_name>.*) metadata for "(?P<path>.*)" '
        r"(?P<item>file|directory) in space "
        r'"(?P<space>.*)" does not contain (?P<val>.*) in (?P<host>.*)'
    )
)
def assert_no_such_metadata_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    users: Users,
    space: str,
    tmp_memory: TmpMemory,
    path: str,
    host: str,
    hosts: Hosts,
    val: str,
    tab_name: str,
    item: str,
) -> None:
    full_path = f"{space}/{path}"
    client_lower = client.lower()
    if client_lower == "web gui":
        tab_name = tab_name.upper() if tab_name != "xattrs" else tab_name
        assert_such_metadata_not_exist_in_op_gui(
            selenium,
            user,
            path,
            tmp_memory,
            space,
            tab_name,
            val,
            item,
        )
    elif client_lower == "rest":
        assert_no_such_metadata_in_op_rest(
            user,
            _as_metadata_users(users),
            host,
            _as_metadata_hosts(hosts),
            full_path,
            tab_name,
            val,
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_no_such_metadata_in_op_oneclient(
            user, users, oneclient_host, full_path, tab_name, val
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r'using (?P<client>.*), (?P<user>\w+) uploads "(?P<path>.*)" '
        r'to "(?P<space>.*)" in (?P<host>.*)'
    )
)
def upload_file_to_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    path: str,
    space: str,
    tmp_memory: TmpMemory,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        successfully_upload_file_to_op_gui(
            path,
            selenium,
            user,
            space,
            tmp_memory,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) uploads local file "
        r'"(?P<path>.*)" to "(?P<space>.*)"'
    )
)
def upload_local_file_to_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    path: str,
    tmpdir: LocalPath,
    space: str,
    tmp_memory: TmpMemory,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        go_to_filebrowser(selenium, user, tmp_memory, space)
        upload_file_to_cwd_in_data_tab(selenium, user, path, tmpdir)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that owner\'s UID "
        r'and GID for "(?P<path>.*)" in space "(?P<space>[\w-]+)" '
        r"are (?P<res>equal|not equal) to (?P<uid>[\d]+) and "
        r"(?P<gid>[\d]+) respectively"
    )
)
def assert_file_stats(
    client: str,
    user: str,
    path: str,
    space: str,
    uid: str,
    gid: str,
    res: str,
    users: Users,
) -> None:
    full_path = f"{space}/{path}"
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.assert_file_ownership(
            user, full_path, res, uid, gid, oneclient_host, users
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


# TODO VFS-12393 uncomment after implementing "assert_file_uid" function
# @wt(
#     parsers.re(
#         r"using (?P<client>.*), (?P<user>\w+) sees that owner\'s UID "
#         r'for "(?P<path>.*)" in space "(?P<space>.*)" '
#         r"is (?P<res>equal|not equal) to (?P<uid>.*)"
#     )
# )
# def assert_file_uid_stat(client, user, path, space, uid, res, users):
#     full_path = f"{space}/{path}"
#     client_lower = client.lower()
#     if "oneclient" in client_lower:
#         oneclient_host = change_client_name_to_hostname(client_lower)
#         multi_file_steps.assert_file_uid(
#             user, full_path, res, uid, oneclient_host, users
#         )
#     else:
#         raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r'using (?P<client>.*), (?P<user>\w+) opens "(?P<path>.*)" '
        r'in space "(?P<space>[\w-]+)" in (?P<host>.*)'
    )
)
def open_path_in_space(
    client: str, user: str, path: str, space: str, users: Users
) -> None:
    full_path = f"{space}/{path}"
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_reg_file_steps.open_file(user, full_path, "664", oneclient_host, users)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.parse('using web GUI, {user} sees that "{owner}" is owner of "{file_name}"')
)
def check_file_owner_web_gui(
    selenium: SeleniumDrivers,
    user: str,
    owner: str,
    file_name: str,
    tmp_memory: TmpMemory,
) -> None:
    check_file_owner(selenium, user, owner, file_name, tmp_memory)
