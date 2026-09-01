"""This module contains gherkin steps to run acceptance tests featuring members
management in Onezone using REST API mixed with web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Mapping

from tests.gui.meta_steps.onezone.members import (
    assert_group_in_space_using_op_gui,
    assert_not_user_in_space_using_op_gui,
    assert_privileges_in_space_using_op_gui,
    fail_to_create_invitation_in_space_using_op_gui,
    fail_to_set_privileges_using_op_gui,
)
from tests.gui.meta_steps.onezone.spaces import add_group_to_space_or_group
from tests.gui.utils.common.constants import WAIT_FRONTEND
from tests.mixed.steps.rest.onezone.members import (
    add_group_to_space_using_rest,
    assert_group_in_space_using_rest,
    assert_not_user_in_space_using_rest,
    assert_privileges_in_space_using_rest,
    fail_to_create_invitation_in_space_using_rest,
    fail_to_set_privileges_using_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) fails to set following "
        r'privileges for "(?P<member_name>.*)" '
        r'(?P<member_type>user|group) in space "(?P<space_name>.*)" in '
        r'"(?P<host>.+?)" Onezone service:\n(?P<config>(.|\s)*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_set_privileges_in_space_in_oz(
    client: str,
    user: str,
    member_name: str,
    member_type: str,
    config: str,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    space_name: str,
    users: Users,
    spaces: Mapping[str, str],
    host: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        fail_to_set_privileges_using_op_gui(
            user,
            space_name,
            member_name,
            member_type,
            config,
            selenium,
        )

    elif client_lower == "rest":
        fail_to_set_privileges_using_rest(
            user, users, hosts, host, spaces, space_name, member_name, config
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees following privileges"
        r' of "(?P<member_name>.*)" (?P<member_type>user|group) in space'
        r' "(?P<space_name>.*)" in "(?P<host>.+?)" Onezone '
        r"service:\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_privileges_in_space_in_oz(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    hosts: Hosts,
    member_name: str,
    users: Users,
    member_type: str,
    config: str,
    spaces: Mapping[str, str],
    host: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_privileges_in_space_using_op_gui(
            user,
            space_name,
            member_name,
            member_type,
            config,
            selenium,
        )
    elif client_lower == "rest":
        assert_privileges_in_space_using_rest(
            user, users, hosts, host, spaces, space_name, member_name, config
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) fails to invite "
        r'"(?P<member_name>.*)" to "(?P<space_name>.*)" space members'
        r' page in "(?P<host>.+?)" Onezone service'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_create_invitation_in_space_in_oz(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    users: Users,
    hosts: Hosts,
    member_name: str,
    spaces: Mapping[str, str],
    host: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        fail_to_create_invitation_in_space_using_op_gui(user, space_name, selenium)
    elif client_lower == "rest":
        fail_to_create_invitation_in_space_using_rest(
            user, users, hosts, host, spaces, space_name, member_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) does not see "
        r'"(?P<member_name>.*)" user on "(?P<space_name>.*)" space '
        r'members page in "(?P<host>.+?)" Onezone service'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_user_in_space_in_oz(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    member_name: str,
    space_name: str,
    users: Users,
    hosts: Hosts,
    host: str,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_not_user_in_space_using_op_gui(user, space_name, member_name, selenium)

    elif client_lower == "rest":
        assert_not_user_in_space_using_rest(
            user, users, hosts, host, spaces, space_name, member_name
        )

    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r'using (?P<client>.*), (?P<user>.+?) adds "(?P<group_name>.*)" '
        r'to space named "(?P<space_name>.*)" in "(?P<host>.+?)" Onezone service'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_group_to_space_in_oz(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    group_name: str,
    users: Users,
    hosts: Hosts,
    host: str,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        where = "space"
        add_group_to_space_or_group(
            user,
            group_name,
            space_name,
            selenium,
            where,
        )
    elif client_lower == "rest":
        add_group_to_space_using_rest(
            user, users, hosts, host, group_name, spaces, space_name
        )

    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r'using (?P<client>.*), (?P<user>.+?) sees "(?P<group_name>.*)" '
        r'group on "(?P<space_name>.*)" space members page in '
        r'"(?P<host>.+?)" Onezone service'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_in_space_in_oz(
    client: str,
    user: str,
    group_name: str,
    space_name: str,
    host: str,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_group_in_space_using_op_gui(selenium, user, space_name, group_name)
    elif client_lower == "rest":
        assert_group_in_space_using_rest(
            user, users, hosts, host, group_name, spaces, space_name
        )

    else:
        raise NoSuchClientException(f"Client: {client} not found")
