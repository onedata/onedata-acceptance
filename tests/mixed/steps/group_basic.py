"""This module contains gherkin steps to run mixed acceptance tests featuring
basic operation on groups using web GUI and swagger.
"""

__author__ = "Michal Stanisz, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2017-2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json

from tests import OZ_REST_PORT
from tests.gui.meta_steps.onezone.groups import (
    add_subgroups_using_op_gui,
    assert_subgroups_using_op_gui,
    create_group_token_to_invite_user_using_op_gui,
    create_groups_using_op_gui,
    fail_to_add_subgroups_using_op_gui,
    fail_to_rename_groups_using_op_gui,
    fail_to_see_groups_using_op_gui,
    fail_to_see_subgroups_using_op_gui,
    join_group_using_op_gui,
    leave_groups_using_op_gui,
    remove_group,
    remove_subgroups_using_op_gui,
    rename_groups_using_op_gui,
    see_groups_using_op_gui,
)
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils.generic import ELEMENTS_SEQUENCE_PATTERN, parse_elements_sequence
from tests.mixed.steps.rest.onezone.group_management import (
    add_subgroups_using_rest,
    assert_subgroups_using_rest,
    create_group_token_using_rest,
    create_groups_using_rest,
    fail_to_add_subgroups_using_rest,
    fail_to_remove_groups_using_rest,
    fail_to_rename_groups_using_rest,
    fail_to_see_groups_using_rest,
    fail_to_see_subgroups_using_rest,
    join_group_using_rest,
    leave_groups_using_rest,
    remove_groups_using_rest,
    remove_subgroups_using_rest,
    rename_groups_using_rest,
    see_groups_using_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.http_exceptions import HTTPUnauthorized
from tests.utils.rest_utils import get_zone_rest_path, http_post
from tests.utils.user_utils import Users


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) creates groups? "
        rf"(?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def create_groups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
) -> None:

    if client.lower() == "rest":
        create_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        create_groups_using_op_gui(selenium, user, group_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"(?P<user>\w+) creates group "
        r'"(?P<group_name>.*)" using REST using received token in '
        r'"(?P<host>.*)" Onezone service'
    )
)
def create_groups_with_token(
    user: str,
    group_name: str,
    host: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:
    group_type = "team"
    zone_hostname = hosts[host]["hostname"]
    token = tmp_memory[user]["mailbox"].get("token", None)
    data = {"X-Auth-Token": token}
    group_properties = {"name": group_name, "type": group_type}
    _ = http_post(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "groups"),
        headers=data,
        data=json.dumps(group_properties),
    )


@wt(
    parsers.re(
        r'(?P<user>\w+) fails to create group "(?P<group_name>.*)" '
        r'using REST using received token in "(?P<host>.*)" Onezone service'
    )
)
def fail_to_create_group_with_token(
    user: str,
    group_name: str,
    host: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:
    try:
        create_groups_with_token(user, group_name, host, tmp_memory, hosts)
        raise AssertionError(
            "function: create_groups_with_token worked but it should not"
        )
    except HTTPUnauthorized:
        pass


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees( that)?"
        rf" groups? named (?P<group_list>{ELEMENTS_SEQUENCE_PATTERN})( ha(s|ve)"
        r' appeared)? in "(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def assert_groups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
) -> None:

    if client.lower() == "rest":
        see_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        see_groups_using_op_gui(selenium, user, group_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) renames groups? "
        rf"(?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) to "
        rf"(?P<new_names>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
        "new_names": parse_elements_sequence,
    },
)
def rename_groups(
    client: str,
    user: str,
    group_list: list[str],
    new_names: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
) -> None:

    if client.lower() == "rest":
        rename_groups_using_rest(user, users, hosts, group_list, new_names, host)
    elif client.lower() == "web gui":
        rename_groups_using_op_gui(selenium, user, group_list, new_names)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) does not see "
        rf"groups? named (?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def fail_to_see_groups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
) -> None:

    if client.lower() == "rest":
        fail_to_see_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        fail_to_see_groups_using_op_gui(selenium, user, group_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) removes groups? "
        rf"(?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def remove_groups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
) -> None:

    if client.lower() == "rest":
        remove_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        remove_group(selenium, user, group_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) leaves groups? "
        rf"(?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def leave_groups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
) -> None:

    if client.lower() == "rest":
        leave_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        leave_groups_using_op_gui(selenium, user, group_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) adds groups? "
        rf"(?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) as subgroup to group"
        r' "(?P<parent>.*)" in "(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def add_subgroups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    parent: str,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:

    if client.lower() == "rest":
        add_subgroups_using_rest(user, users, hosts, group_list, parent, host)
    elif client.lower() == "web gui":
        add_subgroups_using_op_gui(
            selenium,
            user,
            parent,
            group_list,
            tmp_memory,
            displays,
            clipboard,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) removes subgroups? "
        rf'(?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) from group "(?P<parent>.*)" in'
        r' "(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def remove_subgroups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    parent: str,
) -> None:

    if client.lower() == "rest":
        remove_subgroups_using_rest(user, users, hosts, group_list, parent, host)
    elif client.lower() == "web gui":
        remove_subgroups_using_op_gui(
            selenium,
            user,
            group_list,
            tmp_memory,
            parent,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees groups? "
        rf"(?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) as subgroup to group"
        r' "(?P<parent>.*)" in "(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def assert_subgroups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    parent: str,
) -> None:

    if client.lower() == "rest":
        assert_subgroups_using_rest(user, users, hosts, group_list, parent, host)
    elif client.lower() == "web gui":
        assert_subgroups_using_op_gui(selenium, user, group_list, parent)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) does not see groups? "
        rf"(?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) as subgroup to group"
        r' "(?P<parent>.*)" in "(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def fail_to_see_subgroups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    parent: str,
) -> None:
    if client.lower() == "rest":
        fail_to_see_subgroups_using_rest(user, users, group_list, parent, hosts, host)
    elif client.lower() == "web gui":
        fail_to_see_subgroups_using_op_gui(selenium, user, group_list, parent)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user1>\w+) invites "
        r'(?P<user2>\w+) to group "(?P<group>.*)" in "(?P<host>.*)" Onezone service'
    )
)
def invite_to_group(
    client: str,
    user1: str,
    user2: str,
    group: str,
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:

    if client.lower() == "rest":
        create_group_token_using_rest(
            user1, user2, group, tmp_memory, users, hosts, host
        )
    elif client.lower() == "web gui":
        create_group_token_to_invite_user_using_op_gui(
            selenium,
            user1,
            user2,
            group,
            tmp_memory,
            displays,
            clipboard,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) joins group he "
        r'was invited to in "(?P<host>.*)" Onezone service'
    )
)
def join_group(
    client: str,
    user: str,
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
) -> None:

    if client.lower() == "rest":
        join_group_using_rest(user, tmp_memory, hosts, users, host)
    elif client.lower() == "web gui":
        join_group_using_op_gui(selenium, user, tmp_memory)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) fails to rename"
        rf" groups? (?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) to "
        rf"(?P<new_names>{ELEMENTS_SEQUENCE_PATTERN}) in"
        r' "(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
        "new_names": parse_elements_sequence,
    },
)
def fail_to_rename_groups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    new_names: list[str],
) -> None:

    if client.lower() == "rest":
        fail_to_rename_groups_using_rest(
            user, users, hosts, group_list, new_names, host
        )
    elif client.lower() == "web gui":
        fail_to_rename_groups_using_op_gui(selenium, user, group_list, new_names)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) fails to remove"
        rf" groups? (?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def fail_to_remove_groups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
) -> None:

    if client.lower() == "rest":
        fail_to_remove_groups_using_rest(user, users, hosts, group_list, host)
    # TODO VFS-12393 uncomment after implementing function: "fail_to_remove_groups_using_op_gui"
    #  and writing suitable scenario
    # elif client.lower() == 'web gui':
    #     fail_to_remove_groups_using_op_gui(selenium, user, group_list,
    #                                        tmp_memory)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) fails to join"
        rf" groups? (?P<group_list>{ELEMENTS_SEQUENCE_PATTERN}) as subgroup to group "
        r'"(?P<parent>.*?)" in "(?P<host>.*)" Onezone service'
    ),
    converters={
        "group_list": parse_elements_sequence,
    },
)
def fail_to_add_subgroups(
    client: str,
    user: str,
    group_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    parent: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:

    if client.lower() == "rest":
        fail_to_add_subgroups_using_rest(user, users, hosts, group_list, parent, host)
    elif client.lower() == "web gui":
        fail_to_add_subgroups_using_op_gui(
            selenium,
            user,
            parent,
            group_list,
            tmp_memory,
            displays,
            clipboard,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")
