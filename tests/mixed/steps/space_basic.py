"""This module contains gherkin steps to run acceptance tests featuring
basic operations on spaces in Onezone using REST API mixed with web GUI.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Mapping
from typing import cast

from onezone_client import UserApi
from pytest import FixtureRequest  # pylint: disable=wrong-import-order

from tests.gui.meta_steps.onezone.provider import (
    assert_provider_has_name_and_hostname_in_oz_gui,
)
from tests.gui.meta_steps.onezone.spaces import (
    assert_spaces_have_appeared_in_oz_gui,
    assert_spaces_have_been_renamed_in_oz_gui,
    assert_there_are_no_spaces_in_oz_gui,
    assert_there_is_no_provider_for_space_in_oz_gui,
    assert_user_is_member_of_space_gui,
    create_spaces_in_oz_using_gui,
    invite_other_users_to_space_using_gui,
    join_space_in_oz_using_gui,
    leave_spaces_in_oz_using_gui,
    remove_provider_support_for_space_in_oz_using_gui,
    rename_spaces_in_oz_using_gui,
)
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils.generic import ELEMENTS_SEQUENCE_PATTERN, parse_elements_sequence
from tests.mixed.steps.oneclient.data_basic import change_client_name_to_hostname
from tests.mixed.steps.rest.onezone.members import (
    add_users_to_space_in_oz_using_rest,
    assert_user_is_member_of_space_rest,
    delete_users_from_space_in_oz_using_rest,
    invite_other_users_to_space_using_rest,
)
from tests.mixed.steps.rest.onezone.provider import (
    HostsConfig,
    assert_provider_has_name_and_hostname_in_oz_rest,
)
from tests.mixed.steps.rest.onezone.space_management import (
    CredentialsLike,
    assert_spaces_have_appeared_in_oz_rest,
    assert_spaces_have_been_renamed_in_oz_rest,
    assert_there_are_no_spaces_in_oz_rest,
    assert_there_is_no_provider_for_space_in_oz_rest,
    create_spaces_in_oz_using_rest,
    join_space_in_oz_using_rest,
    leave_spaces_in_oz_using_rest,
    remove_provider_support_for_space_in_oz_using_rest,
    remove_spaces_in_oz_using_rest,
    rename_spaces_in_oz_using_rest,
)
from tests.mixed.type_definitions import MutableSpaces as Spaces
from tests.mixed.utils.common import NoSuchClientException, login_to_oz
from tests.oneclient.steps.multi_file_steps import ls_present_spaces
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import User, Users
from tests.utils.utils import repeat_failed


def _as_space_users(users: Users) -> Users:
    return users


def _as_member_users(users: Users) -> Users:
    return users


def _as_provider_users(users: Users) -> Users:
    return users


def _as_credentials(credentials: User) -> CredentialsLike:
    return cast(CredentialsLike, credentials)


def _as_provider_hosts(hosts: Hosts) -> HostsConfig:
    return cast(HostsConfig, hosts)


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) creates "
        rf"spaces? (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.+?)" Onezone service'
    ),
    converters={
        "space_list": parse_elements_sequence,
    },
)
def create_spaces_in_oz(
    client: str,
    user: str,
    space_list: list[str],
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    spaces: Spaces,
    clipboard: Clipboard,
    displays: dict[str, str],
    request: FixtureRequest,
    admin_credentials: CredentialsLike,
) -> None:

    if client.lower() == "rest":
        create_spaces_in_oz_using_rest(
            user,
            _as_space_users(users),
            hosts,
            host,
            space_list,
            spaces,
            request,
            admin_credentials,
        )
    elif client.lower() == "web gui":

        create_spaces_in_oz_using_gui(
            selenium,
            user,
            space_list,
            spaces,
            clipboard,
            displays,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) leaves spaces? "
        rf"named (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.+?)" Onezone service'
    ),
    converters={
        "space_list": parse_elements_sequence,
    },
)
def leave_spaces_in_oz(
    client: str,
    user: str,
    space_list: list[str],
    host: str,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    spaces: Spaces,
) -> None:

    if client.lower() == "rest":

        leave_spaces_in_oz_using_rest(
            user, _as_space_users(users), host, hosts, space_list, spaces
        )
    elif client.lower() == "web gui":

        leave_spaces_in_oz_using_gui(selenium, user, space_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) renames spaces? "
        rf"named (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) to"
        rf" (?P<new_names_list>{ELEMENTS_SEQUENCE_PATTERN}) "
        r'in "(?P<host>.+?)" Onezone service'
    ),
    converters={
        "new_names_list": parse_elements_sequence,
        "space_list": parse_elements_sequence,
    },
)
def rename_spaces_in_oz(
    client: str,
    user: str,
    space_list: list[str],
    new_names_list: list[str],
    host: str,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    spaces: Spaces,
) -> None:

    if client.lower() == "rest":

        rename_spaces_in_oz_using_rest(
            user,
            _as_space_users(users),
            host,
            hosts,
            space_list,
            new_names_list,
            spaces,
        )
    elif client.lower() == "web gui":

        rename_spaces_in_oz_using_gui(selenium, user, space_list, new_names_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) removes spaces? "
        rf"named (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.+?)" Onezone service'
    ),
    converters={
        "space_list": parse_elements_sequence,
    },
)
@wt(
    parsers.re(
        r"using (?P<client>.*), user of (?P<user>.+?) removes spaces? "
        rf"named (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.+?)" Onezone service'
    ),
    converters={
        "space_list": parse_elements_sequence,
    },
)
def remove_spaces_in_oz(
    client: str,
    user: str,
    space_list: list[str],
    host: str,
    users: Users,
    hosts: Hosts,
    spaces: Spaces,
) -> None:

    if client.lower() == "rest":

        remove_spaces_in_oz_using_rest(
            user, _as_space_users(users), host, hosts, space_list, spaces
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) removes "
        rf"(?P<user_list>{ELEMENTS_SEQUENCE_PATTERN}) from space"
        r' "(?P<space_name>.+?)" in '
        r'"(?P<host>.+?)" Onezone service'
    ),
    converters={
        "user_list": parse_elements_sequence,
    },
)
def delete_users_from_space_in_oz(
    client: str,
    user_list: list[str],
    space_name: str,
    host: str,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
    user: str,
) -> None:

    if client.lower() == "rest":

        delete_users_from_space_in_oz_using_rest(
            user_list, _as_member_users(users), host, hosts, space_name, spaces, user
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) adds "
        rf'(?P<user_list>{ELEMENTS_SEQUENCE_PATTERN}) to "(?P<space_name>.+?)" in '
        r'"(?P<host>.+?)" Onezone service'
    ),
    converters={
        "user_list": parse_elements_sequence,
    },
)
def add_users_to_space_in_oz(
    client: str,
    user_list: list[str],
    space_name: str,
    host: str,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
    user: str,
) -> None:

    if client.lower() == "rest":

        add_users_to_space_in_oz_using_rest(
            user_list, _as_member_users(users), host, hosts, space_name, spaces, user
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) removes support "
        r'from provider "(?P<provider_name>.+?)" for space named '
        r'"(?P<space_name>.+?)" in "(?P<host>.+?)" Onezone service'
    )
)
def remove_provider_support_for_space_in_oz(
    client: str,
    user: str,
    provider_name: str,
    space_name: str,
    host: str,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    spaces: Spaces,
    admin_credentials: User,
) -> None:

    if client.lower() == "rest":

        remove_provider_support_for_space_in_oz_using_rest(
            user,
            _as_space_users(users),
            host,
            hosts,
            provider_name,
            space_name,
            spaces,
            _as_credentials(admin_credentials),
        )
    elif client.lower() == "web gui":

        remove_provider_support_for_space_in_oz_using_gui(
            selenium, user, space_name, hosts
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) invites "
        rf"(?P<user_list>{ELEMENTS_SEQUENCE_PATTERN}) to space named"
        r' "(?P<space_name>.+?)" in '
        r'"(?P<host>.+?)" Onezone service'
    ),
    converters={"user_list": parse_elements_sequence},
)
def invite_other_users_to_space(
    client: str,
    user: str,
    user_list: list[str],
    space_name: str,
    host: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:

    if client.lower() == "rest":

        for invited_user in user_list:
            invite_other_users_to_space_using_rest(
                user,
                _as_member_users(users),
                host,
                hosts,
                space_name,
                spaces,
                tmp_memory,
                invited_user,
            )

    elif client.lower() == "web gui":

        invite_other_users_to_space_using_gui(
            selenium,
            user,
            space_name,
            user_list,
            tmp_memory,
            displays,
            clipboard,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        rf"using (?P<client>.*), (?P<user_list>{ELEMENTS_SEQUENCE_PATTERN}) joins to "
        r'space using received (?P<item_name>.+?) in "(?P<host>.+?)" Onezone service'
    ),
    converters={
        "user_list": parse_elements_sequence,
    },
)
def join_space_in_oz(
    client: str,
    user_list: list[str],
    item_name: str,
    host: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
) -> None:

    if client.lower() == "rest":

        join_space_in_oz_using_rest(
            user_list, _as_space_users(users), host, hosts, item_name, tmp_memory
        )
    elif client.lower() == "web gui":

        join_space_in_oz_using_gui(selenium, user_list, tmp_memory)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that "
        rf"spaces? named (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) (has|have)"
        r' appeared in "(?P<host>.+?)" Onezone service'
    ),
    converters={
        "space_list": parse_elements_sequence,
    },
)
def assert_there_are_spaces_in_oz(
    client: str,
    user: str,
    space_list: list[str],
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    host: str,
) -> None:

    if client.lower() == "web gui":

        assert_spaces_have_appeared_in_oz_gui(selenium, user, space_list)
    elif client.lower() == "rest":

        assert_spaces_have_appeared_in_oz_rest(
            user, _as_space_users(users), hosts, host, space_list
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that "
        rf"spaces? named (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) (has|have)"
        r' disappeared from "(?P<host>.+?)" Onezone service'
    ),
    converters={
        "space_list": parse_elements_sequence,
    },
)
def assert_there_are_no_spaces_in_oz(
    client: str,
    user: str,
    space_list: list[str],
    host: str,
    selenium: SeleniumDrivers,
    users: Users,
    spaces: Spaces,
    hosts: Hosts,
) -> None:

    if client.lower() == "rest":

        assert_there_are_no_spaces_in_oz_rest(
            user, _as_space_users(users), host, hosts, space_list, spaces
        )
    elif client.lower() == "web gui":

        assert_there_are_no_spaces_in_oz_gui(selenium, user, space_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that "
        rf"spaces? named (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) "
        r"(has|have) been renamed to "
        rf"(?P<new_names_list>{ELEMENTS_SEQUENCE_PATTERN}) in "
        r'"(?P<host>.+?)" Onezone service'
    ),
    converters={
        "new_names_list": parse_elements_sequence,
        "space_list": parse_elements_sequence,
    },
)
def assert_spaces_have_been_renamed_in_oz(
    client: str,
    user: str,
    space_list: list[str],
    new_names_list: list[str],
    host: str,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    spaces: Spaces,
) -> None:

    if client.lower() == "rest":

        assert_spaces_have_been_renamed_in_oz_rest(
            user,
            _as_space_users(users),
            host,
            hosts,
            space_list,
            new_names_list,
            spaces,
        )
    elif client.lower() == "web gui":

        assert_spaces_have_been_renamed_in_oz_gui(
            selenium, user, space_list, new_names_list
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that there "
        r"(is|are) no supporting providers? "
        rf"(?P<providers_list>{ELEMENTS_SEQUENCE_PATTERN}) for space named "
        r'"(?P<space_name>.+?)" in "(?P<host>.+?)" Onezone service'
    ),
    converters={
        "providers_list": parse_elements_sequence,
    },
)
def assert_there_is_no_provider_for_space_in_oz(
    client: str,
    user: str,
    providers_list: list[str],
    space_name: str,
    host: str,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    spaces: Spaces,
    admin_credentials: User,
) -> None:

    if client.lower() == "rest":

        assert_there_is_no_provider_for_space_in_oz_rest(
            user,
            _as_space_users(users),
            host,
            hosts,
            space_name,
            spaces,
            providers_list,
            _as_credentials(admin_credentials),
        )
    elif client.lower() == "web gui":

        assert_there_is_no_provider_for_space_in_oz_gui(selenium, user, space_name)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that "
        rf"(?P<user_list>{ELEMENTS_SEQUENCE_PATTERN}) (is|are) members? of "
        r'"(?P<space_name>.+?)" in "(?P<host>.+?)" Onezone service'
    ),
    converters={
        "user_list": parse_elements_sequence,
    },
)
def assert_user_is_member_of_space(
    client: str,
    user: str,
    user_list: list[str],
    space_name: str,
    host: str,
    spaces: Mapping[str, str],
    users: Users,
    hosts: Hosts,
    selenium: SeleniumDrivers,
) -> None:

    if client.lower() == "rest":

        assert_user_is_member_of_space_rest(
            space_name, spaces, user, _as_member_users(users), user_list, host, hosts
        )
    elif client.lower() == "web gui":

        assert_user_is_member_of_space_gui(selenium, user, space_name, user_list)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees provider "
        r'"(?P<provider_name>.+?)" with hostname matches that of '
        r'"(?P<provider>.+?)" provider in "(?P<host>.+?)" Onezone service'
    )
)
def assert_provider_has_given_name_and_known_hostname_in_oz(
    client: str,
    user: str,
    provider_name: str,
    provider: str,
    host: str,
    users: Users,
    hosts: Hosts,
    selenium: SeleniumDrivers,
) -> None:

    provider_name = hosts[provider_name]["name"]

    if client.lower() == "rest":

        assert_provider_has_name_and_hostname_in_oz_rest(
            user,
            _as_provider_users(users),
            host,
            _as_provider_hosts(hosts),
            provider_name,
            hosts[provider]["hostname"],
        )
    elif client.lower() == "web gui":

        assert_provider_has_name_and_hostname_in_oz_gui(
            selenium, user, provider_name, provider, hosts
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.parse(
        'using {client}, {user} sees spaces "{expected_spaces}" in mount point'
    )
)
def assert_spaces_in_mount_point(
    client: str, user: str, users: Users, expected_spaces: str
) -> None:
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        ls_present_spaces(user, list_parser(expected_spaces), oneclient_host, users)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.parse(
        'using {client}, {user} sees spaces "{expected_spaces}" in mount point, '
        "waiting up to {timeout:d}s"
    )
)
def assert_spaces_in_mount_point_with_waiting(
    client: str, user: str, users: Users, expected_spaces: str, timeout: int
) -> None:
    @repeat_failed(timeout=timeout)
    def assert_with_timeout() -> None:
        assert_spaces_in_mount_point(client, user, users, expected_spaces)

    assert_with_timeout()


@wt(
    parsers.parse(
        'using {client}, {user} sees spaces "{expected_spaces}" from "{zone_name}"'
        " Onezone service, annotated with their ids in mount point"
    )
)
def assert_spaces_with_ids_in_mount_point(
    client: str,
    user: str,
    users: Users,
    expected_spaces: str,
    zone_name: str,
    hosts: Hosts,
) -> None:
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        user_client = login_to_oz(
            user, users[user].password, hosts[zone_name]["hostname"]
        )

        user_api = UserApi(user_client)
        user_spaces = user_api.list_user_spaces().spaces

        space_names_with_ids = []
        expected_space_names = list_parser(expected_spaces)
        for sid in user_spaces:
            space = user_api.get_user_space(sid)
            if space.name in expected_space_names:
                space_names_with_ids.append(f"{space.name}@{space.space_id}")

        ls_present_spaces(user, space_names_with_ids, oneclient_host, users)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.parse(
        'using {client}, {user} sees spaces "{expected_spaces}" from "{zone_name}"'
        " Onezone service, annotated with their ids in mount point, "
        "waiting up to {timeout:d}s"
    )
)
def assert_spaces_with_ids_in_mount_point_with_waiting(
    client: str,
    user: str,
    users: Users,
    expected_spaces: str,
    zone_name: str,
    hosts: Hosts,
    timeout: int,
) -> None:
    @repeat_failed(timeout=timeout)
    def assert_with_timeout() -> None:
        assert_spaces_with_ids_in_mount_point(
            client, user, users, expected_spaces, zone_name, hosts
        )

    assert_with_timeout()
