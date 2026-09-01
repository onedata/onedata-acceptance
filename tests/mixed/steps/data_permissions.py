"""This module contains gherkin steps to run mixed acceptance tests featuring
basic operations on permissions on data using web GUI and REST.
"""

__author__ = "Michal Stanisz, Michal Cwiertnia, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from collections.abc import Mapping

from tests.gui.meta_steps.oneprovider.permissions import (
    assert_ace_in_op_gui,
    assert_posix_permissions_in_op_gui,
    fail_to_set_posix_permissions_in_op_gui,
    grant_acl_privileges_in_op_gui,
    set_posix_permissions_in_op_gui,
)
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils.common.constants import WAIT_BACKEND
from tests.mixed.steps.data_basic import change_client_name_to_hostname
from tests.mixed.steps.oneclient.data_basic import (
    assert_ace_in_op_oneclient,
    assert_posix_permissions_in_op_oneclient,
    grant_acl_privileges_in_op_oneclient,
    set_posix_permissions_in_op_oneclient,
)
from tests.mixed.steps.rest.oneprovider.data import (
    assert_ace_in_op_rest,
    assert_posix_permissions_in_op_rest,
    grant_acl_privileges_in_op_rest,
    set_posix_permissions_in_op_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


def _remove_parent_acl_from_string(privileges: str) -> str:
    return re.sub("[a-zA-Z]+:", "", privileges)


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sets new ACE for "
        r'(?P<path>.*?) in space "(?P<space>.*)" with (?P<privileges>.*) '
        r"privileges? set for (?P<item_type>.*?) (?P<name>.*) in (?P<host>.*)"
    )
)
def grant_acl_privileges_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    space: str,
    path: str,
    host: str,
    hosts: Hosts,
    users: Users,
    privileges: str,
    item_type: str,
    name: str,
    groups: Mapping[str, str],
    tmp_memory: TmpMemory,
) -> None:
    full_path = f"{space}/{path}"
    client_lower = client.lower()

    if client_lower == "web gui":
        grant_acl_privileges_in_op_gui(
            selenium,
            user,
            path,
            privileges,
            name,
            tmp_memory,
            space,
        )
    elif client_lower == "rest":
        privileges = _remove_parent_acl_from_string(privileges)
        grant_acl_privileges_in_op_rest(
            user,
            users,
            host,
            hosts,
            full_path,
            privileges,
            item_type,
            name,
            groups,
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        privileges = _remove_parent_acl_from_string(privileges)
        grant_acl_privileges_in_op_oneclient(
            user,
            users,
            oneclient_host,
            full_path,
            privileges,
            item_type,
            groups,
            name,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees that (?P<path>.*?)"
        r' in space "(?P<space>.*)" (has|have) (?P<privileges>.*) '
        r"privileges? set for (?P<item_type>.*?) (?P<name>.*) in "
        r"(?P<num>.*) ACL record in (?P<host>.*)"
    )
)
def assert_ace_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    space: str,
    path: str,
    host: str,
    hosts: Hosts,
    users: Users,
    num: str,
    privileges: str,
    item_type: str,
    name: str,
    tmp_memory: TmpMemory,
) -> None:
    full_path = f"{space}/{path}"
    client_lower = client.lower()

    if client_lower == "web gui":
        assert_ace_in_op_gui(
            selenium,
            user,
            privileges,
            item_type,
            name,
            num,
            space,
            path,
            tmp_memory,
        )
    elif client_lower == "rest":
        privileges = _remove_parent_acl_from_string(privileges)
        assert_ace_in_op_rest(
            user,
            users,
            host,
            hosts,
            full_path,
            num,
            privileges,
            item_type,
            name,
        )
    elif "oneclient" in client_lower:
        privileges = _remove_parent_acl_from_string(privileges)
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_ace_in_op_oneclient(
            user,
            users,
            oneclient_host,
            full_path,
            num,
            privileges,
            item_type,
            name,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees "
        r'that POSIX permission for item named "(?P<item_path>.*)" in '
        r'"(?P<space>.*)" is "(?P<mode>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_posix_permissions_in_op(
    client: str,
    user: str,
    item_path: str,
    space: str,
    mode: str,
    host: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
) -> None:
    full_path = f"{space}/{item_path}"
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_posix_permissions_in_op_gui(
            selenium,
            user,
            space,
            item_path,
            mode,
            tmp_memory,
        )
    elif client_lower == "rest":
        assert_posix_permissions_in_op_rest(full_path, mode, user, users, host, hosts)
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_posix_permissions_in_op_oneclient(
            user, full_path, mode, oneclient_host, users
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to set "
        r'"(?P<mode>.*)" POSIX permission for item named '
        r'"(?P<item_path>.*)" in "(?P<space>.*)" in (?P<host>.*)'
    )
)
def set_posix_permissions_in_op(
    client: str,
    user: str,
    item_path: str,
    space: str,
    mode: str,
    result: str,
    host: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
) -> None:
    full_path = f"{space}/{item_path}"
    client_lower = client.lower()
    if client_lower == "web gui":
        if result == "fails":
            fail_to_set_posix_permissions_in_op_gui(
                selenium,
                user,
                space,
                item_path,
                mode,
                tmp_memory,
            )
        else:
            set_posix_permissions_in_op_gui(
                selenium,
                user,
                space,
                item_path,
                mode,
                tmp_memory,
            )
    elif client_lower == "rest":
        set_posix_permissions_in_op_rest(
            full_path, mode, user, users, host, hosts, result
        )
    elif "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        set_posix_permissions_in_op_oneclient(
            user, full_path, mode, oneclient_host, users, result
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")
