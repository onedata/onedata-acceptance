"""This module contains gherkin steps to run mixed acceptance tests featuring
basic operation on groups using web GUI and swagger.
"""

__author__ = "Michal Stanisz, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2017-2019 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

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
from tests.utils.bdd_utils import parsers, wt
from tests.utils.http_exceptions import HTTPUnauthorized
from tests.utils.rest_utils import get_zone_rest_path, http_post


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) creates groups? "
        '(?P<group_list>.*) in "(?P<host>.*)" Onezone service'
    )
)
def create_groups(
    client, user, group_list, host, hosts, users, selenium, oz_page
):

    if client.lower() == "rest":
        create_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        create_groups_using_op_gui(selenium, user, group_list, oz_page)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"(?P<user>\w+) creates group "
        '"(?P<group_name>.*)" using REST using received token in '
        '"(?P<host>.*)" Onezone service'
    )
)
def create_groups_with_token(user, group_name, host, tmp_memory, hosts):
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
        r'using REST using received token in "(?P<host>.*)" Onezone'
        r" service"
    )
)
def fail_to_create_group_with_token(user, group_name, host, tmp_memory, hosts):
    try:
        create_groups_with_token(user, group_name, host, tmp_memory, hosts)
        raise AssertionError(
            "function: create_groups_with_token worked but it should not"
        )
    except HTTPUnauthorized as err:
        if err.status_code == 404:
            pass


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees( that)?"
        " groups? named (?P<group_list>.*?)( ha(s|ve) appeared)? in"
        ' "(?P<host>.*)" Onezone service'
    )
)
def assert_groups(
    client, user, group_list, host, hosts, users, selenium, oz_page
):

    if client.lower() == "rest":
        see_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        see_groups_using_op_gui(selenium, user, oz_page, group_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) renames groups? "
        "(?P<group_list>.*)to (?P<new_names>.*) in "
        '"(?P<host>.*)" Onezone service'
    )
)
def rename_groups(
    client,
    user,
    group_list,
    new_names,
    host,
    hosts,
    users,
    selenium,
    oz_page,
    popups,
):

    if client.lower() == "rest":
        rename_groups_using_rest(
            user, users, hosts, group_list, new_names, host
        )
    elif client.lower() == "web gui":
        rename_groups_using_op_gui(
            selenium, user, oz_page, group_list, new_names, popups
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) does not see "
        'groups? named (?P<group_list>.*) in "(?P<host>.*)" '
        "Onezone service"
    )
)
def fail_to_see_groups(
    client, user, group_list, host, hosts, users, selenium, oz_page
):

    if client.lower() == "rest":
        fail_to_see_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        fail_to_see_groups_using_op_gui(selenium, user, oz_page, group_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) removes groups? "
        '(?P<group_list>.*) in "(?P<host>.*)" Onezone service'
    )
)
def remove_groups(
    client, user, group_list, host, hosts, users, selenium, oz_page, popups
):

    if client.lower() == "rest":
        remove_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        remove_group(selenium, user, group_list, oz_page, popups)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) leaves groups? "
        '(?P<group_list>.*) in "(?P<host>.*)" Onezone service'
    )
)
def leave_groups(
    client, user, group_list, host, hosts, users, selenium, oz_page, popups
):

    if client.lower() == "rest":
        leave_groups_using_rest(user, users, hosts, group_list, host)
    elif client.lower() == "web gui":
        leave_groups_using_op_gui(selenium, user, oz_page, group_list, popups)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) adds groups? "
        '(?P<group_list>.*) as subgroup to group "(?P<parent>.*)" in'
        ' "(?P<host>.*)" Onezone service'
    )
)
def add_subgroups(
    client,
    user,
    group_list,
    host,
    hosts,
    users,
    selenium,
    oz_page,
    tmp_memory,
    parent,
    displays,
    clipboard,
    onepanel,
    popups,
):

    if client.lower() == "rest":
        add_subgroups_using_rest(user, users, hosts, group_list, parent, host)
    elif client.lower() == "web gui":
        add_subgroups_using_op_gui(
            selenium,
            user,
            oz_page,
            parent,
            group_list,
            tmp_memory,
            displays,
            clipboard,
            onepanel,
            popups,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) removes subgroups? "
        '(?P<group_list>.*) from group "(?P<parent>.*)" in'
        ' "(?P<host>.*)" Onezone service'
    )
)
def remove_subgroups(
    client,
    user,
    group_list,
    host,
    hosts,
    users,
    selenium,
    oz_page,
    tmp_memory,
    parent,
    onepanel,
    popups,
):

    if client.lower() == "rest":
        remove_subgroups_using_rest(
            user, users, hosts, group_list, parent, host
        )
    elif client.lower() == "web gui":
        remove_subgroups_using_op_gui(
            selenium,
            user,
            oz_page,
            group_list,
            tmp_memory,
            parent,
            onepanel,
            popups,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) sees groups? "
        '(?P<group_list>.*) as subgroup to group "(?P<parent>.*)" '
        'in "(?P<host>.*)" Onezone service'
    )
)
def assert_subgroups(
    client,
    user,
    group_list,
    host,
    hosts,
    users,
    selenium,
    parent,
    oz_page,
    onepanel,
):

    if client.lower() == "rest":
        assert_subgroups_using_rest(
            user, users, hosts, group_list, parent, host
        )
    elif client.lower() == "web gui":
        assert_subgroups_using_op_gui(
            selenium, user, oz_page, group_list, parent, onepanel
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) does not see groups? "
        '(?P<group_list>.*) as subgroup to group "(?P<parent>.*)"'
        ' in "(?P<host>.*)" Onezone service'
    )
)
def fail_to_see_subgroups(
    client,
    user,
    group_list,
    host,
    hosts,
    users,
    selenium,
    oz_page,
    parent,
    onepanel,
):

    if client.lower() == "rest":
        fail_to_see_subgroups_using_rest(
            user, users, group_list, parent, hosts, host
        )
    elif client.lower() == "web gui":
        fail_to_see_subgroups_using_op_gui(
            selenium, user, oz_page, group_list, parent, onepanel
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user1>\w+) invites "
        r'(?P<user2>\w+) to group "(?P<group>.*)" in "(?P<host>.*)" '
        r"Onezone service"
    )
)
def invite_to_group(
    client,
    user1,
    user2,
    group,
    host,
    hosts,
    users,
    selenium,
    oz_page,
    tmp_memory,
    displays,
    clipboard,
    onepanel,
    popups,
):

    if client.lower() == "rest":
        create_group_token_using_rest(
            user1, user2, group, tmp_memory, users, hosts, host
        )
    elif client.lower() == "web gui":
        create_group_token_to_invite_user_using_op_gui(
            selenium,
            user1,
            user2,
            oz_page,
            group,
            tmp_memory,
            displays,
            clipboard,
            onepanel,
            popups,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) joins group he "
        'was invited to in "(?P<host>.*)" Onezone service'
    )
)
def join_group(client, user, host, hosts, users, selenium, oz_page, tmp_memory):

    if client.lower() == "rest":
        join_group_using_rest(user, tmp_memory, hosts, users, host)
    elif client.lower() == "web gui":
        join_group_using_op_gui(selenium, user, oz_page, tmp_memory)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) fails to rename"
        " groups? (?P<group_list>.*) to (?P<new_names>.*) in"
        ' "(?P<host>.*)" Onezone service'
    )
)
def fail_to_rename_groups(
    client,
    user,
    group_list,
    host,
    hosts,
    users,
    selenium,
    oz_page,
    new_names,
    popups,
):

    if client.lower() == "rest":
        fail_to_rename_groups_using_rest(
            user, users, hosts, group_list, new_names, host
        )
    elif client.lower() == "web gui":
        fail_to_rename_groups_using_op_gui(
            selenium, user, oz_page, group_list, new_names, popups
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) fails to remove"
        ' groups? (?P<group_list>.*?) in "(?P<host>.*)" Onezone service'
    )
)
def fail_to_remove_groups(
    client,
    user,
    group_list,
    host,
    hosts,
    users,
):

    if client.lower() == "rest":
        fail_to_remove_groups_using_rest(user, users, hosts, group_list, host)
    # TODO VFS-12393 uncomment after implementing function: "fail_to_remove_groups_using_op_gui"
    #  and writing suitable scenario
    # elif client.lower() == 'web gui':
    #     fail_to_remove_groups_using_op_gui(selenium, user, op_container, group_list,
    #                                        tmp_memory)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) fails to join"
        " groups? (?P<group_list>.*?) as subgroup to group "
        '"(?P<parent>.*?)" in "(?P<host>.*)" Onezone service'
    )
)
def fail_to_add_subgroups(
    client,
    user,
    group_list,
    host,
    hosts,
    users,
    selenium,
    oz_page,
    parent,
    tmp_memory,
    displays,
    clipboard,
    onepanel,
    popups,
):

    if client.lower() == "rest":
        fail_to_add_subgroups_using_rest(
            user, users, hosts, group_list, parent, host
        )
    elif client.lower() == "web gui":
        fail_to_add_subgroups_using_op_gui(
            selenium,
            user,
            oz_page,
            parent,
            group_list,
            tmp_memory,
            displays,
            clipboard,
            onepanel,
            popups,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")
