"""This module contains gherkin steps to run acceptance tests featuring
basic operations on spaces in Onezone using REST API mixed with web GUI.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

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
from tests.mixed.steps.rest.onezone.members import (
    add_users_to_space_in_oz_using_rest,
    assert_user_is_member_of_space_rest,
    delete_users_from_space_in_oz_using_rest,
    invite_other_users_to_space_using_rest,
)
from tests.mixed.steps.rest.onezone.provider import (
    assert_provider_has_name_and_hostname_in_oz_rest,
)
from tests.mixed.steps.rest.onezone.space_management import (
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
from tests.mixed.utils.common import NoSuchClientException
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) creates "
        'spaces? (?P<space_list>.+?) in "(?P<host>.+?)" '
        "Onezone service"
    )
)
def create_spaces_in_oz(
    client,
    user,
    space_list,
    host,
    hosts,
    users,
    selenium,
    oz_page,
    spaces,
    popups,
    clipboard,
    displays,
):

    if client.lower() == "rest":

        create_spaces_in_oz_using_rest(user, users, hosts, host, space_list)
    elif client.lower() == "web gui":

        create_spaces_in_oz_using_gui(
            selenium,
            user,
            oz_page,
            space_list,
            spaces,
            popups,
            clipboard,
            displays,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) leaves spaces? "
        'named (?P<space_list>.+?) in "(?P<host>.+?)" Onezone '
        "service"
    )
)
def leave_spaces_in_oz(
    client,
    user,
    space_list,
    host,
    selenium,
    oz_page,
    users,
    hosts,
    spaces,
    popups,
    modals,
):

    if client.lower() == "rest":

        leave_spaces_in_oz_using_rest(
            user, users, host, hosts, space_list, spaces
        )
    elif client.lower() == "web gui":

        leave_spaces_in_oz_using_gui(
            selenium, user, space_list, oz_page, popups, modals
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) renames spaces? "
        "named (?P<space_list>.+?) to (?P<new_names_list>.+?) "
        'in "(?P<host>.+?)" Onezone service'
    )
)
def rename_spaces_in_oz(
    client,
    user,
    space_list,
    new_names_list,
    host,
    selenium,
    oz_page,
    users,
    hosts,
    spaces,
):

    if client.lower() == "rest":

        rename_spaces_in_oz_using_rest(
            user, users, host, hosts, space_list, new_names_list, spaces
        )
    elif client.lower() == "web gui":

        rename_spaces_in_oz_using_gui(
            selenium, user, oz_page, space_list, new_names_list
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) removes spaces? "
        'named (?P<space_list>.+?) in "(?P<host>.+?)" Onezone '
        "service"
    )
)
@wt(
    parsers.re(
        "using (?P<client>.*), user of (?P<user>.+?) removes spaces? "
        'named (?P<space_list>.+?) in "(?P<host>.+?)" Onezone '
        "service"
    )
)
def remove_spaces_in_oz(client, user, space_list, host, users, hosts, spaces):

    if client.lower() == "rest":

        remove_spaces_in_oz_using_rest(
            user, users, host, hosts, space_list, spaces
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) removes "
        '(?P<user_list>.+?) from space "(?P<space_name>.+?)" in '
        '"(?P<host>.+?)" Onezone service'
    )
)
def delete_users_from_space_in_oz(
    client, user_list, space_name, host, users, hosts, spaces, user
):

    if client.lower() == "rest":

        delete_users_from_space_in_oz_using_rest(
            user_list, users, host, hosts, space_name, spaces, user
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) adds "
        '(?P<user_list>.+?) to "(?P<space_name>.+?)" in '
        '"(?P<host>.+?)" Onezone service'
    )
)
def add_users_to_space_in_oz(
    client, user_list, space_name, host, users, hosts, spaces, user
):

    if client.lower() == "rest":

        add_users_to_space_in_oz_using_rest(
            user_list, users, host, hosts, space_name, spaces, user
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) removes support "
        'from provider "(?P<provider_name>.+?)" for space named '
        '"(?P<space_name>.+?)" in "(?P<host>.+?)" Onezone service'
    )
)
def remove_provider_support_for_space_in_oz(
    client,
    user,
    provider_name,
    space_name,
    host,
    selenium,
    users,
    hosts,
    spaces,
    admin_credentials,
    onepanel,
    popups,
    modals,
):

    if client.lower() == "rest":

        remove_provider_support_for_space_in_oz_using_rest(
            user,
            users,
            host,
            hosts,
            provider_name,
            space_name,
            spaces,
            admin_credentials,
        )
    elif client.lower() == "web gui":

        remove_provider_support_for_space_in_oz_using_gui(
            selenium, user, space_name, onepanel, popups, hosts, modals
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) invites "
        '(?P<user_list>.+?) to space named "(?P<space_name>.+?)" in '
        '"(?P<host>.+?)" Onezone service'
    )
)
def invite_other_users_to_space(
    client,
    user,
    user_list,
    space_name,
    host,
    selenium,
    tmp_memory,
    users,
    hosts,
    spaces,
    displays,
    clipboard,
    oz_page,
    onepanel,
    popups,
    modals,
):

    if client.lower() == "rest":

        invite_other_users_to_space_using_rest(
            user, users, host, hosts, space_name, spaces, tmp_memory, user_list
        )

    elif client.lower() == "web gui":

        invite_other_users_to_space_using_gui(
            selenium,
            user,
            space_name,
            user_list,
            oz_page,
            tmp_memory,
            displays,
            clipboard,
            onepanel,
            popups,
            modals,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user_list>.+?) joins to "
        'space using received (?P<item_name>.+?) in "(?P<host>.+?)" '
        "Onezone service"
    )
)
def join_space_in_oz(
    client,
    user_list,
    item_name,
    host,
    selenium,
    oz_page,
    tmp_memory,
    users,
    hosts,
):

    if client.lower() == "rest":

        join_space_in_oz_using_rest(
            user_list, users, host, hosts, item_name, tmp_memory
        )
    elif client.lower() == "web gui":

        join_space_in_oz_using_gui(selenium, user_list, oz_page, tmp_memory)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that "
        "spaces? named (?P<space_list>.+?) (has|have) appeared in "
        '"(?P<host>.+?)" Onezone service'
    )
)
def assert_there_are_spaces_in_oz(
    client, user, space_list, selenium, oz_page, users, hosts, host
):

    if client.lower() == "web gui":

        assert_spaces_have_appeared_in_oz_gui(
            selenium, user, oz_page, space_list
        )
    elif client.lower() == "rest":

        assert_spaces_have_appeared_in_oz_rest(
            user, users, hosts, host, space_list
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that "
        "spaces? named (?P<space_list>.+?) (has|have) disappeared "
        'from "(?P<host>.+?)" Onezone service'
    )
)
def assert_there_are_no_spaces_in_oz(
    client,
    user,
    space_list,
    host,
    selenium,
    oz_page,
    users,
    spaces,
    hosts,
):

    if client.lower() == "rest":

        assert_there_are_no_spaces_in_oz_rest(
            user, users, host, hosts, space_list, spaces
        )
    elif client.lower() == "web gui":

        assert_there_are_no_spaces_in_oz_gui(
            selenium, user, oz_page, space_list
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that "
        "spaces? named (?P<space_list>.+?) (has|have) been renamed to "
        '(?P<new_names_list>.+?) in "(?P<host>.+?)" Onezone service'
    )
)
def assert_spaces_have_been_renamed_in_oz(
    client,
    user,
    space_list,
    new_names_list,
    host,
    selenium,
    oz_page,
    users,
    hosts,
    spaces,
):

    if client.lower() == "rest":

        assert_spaces_have_been_renamed_in_oz_rest(
            user, users, host, hosts, space_list, new_names_list, spaces
        )
    elif client.lower() == "web gui":

        assert_spaces_have_been_renamed_in_oz_gui(
            selenium, user, oz_page, space_list, new_names_list
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that there "
        "(is|are) no supporting providers? "
        "(?P<providers_list>.+?) for space named "
        '"(?P<space_name>.+?)" in "(?P<host>.+?)" Onezone service'
    )
)
def assert_there_is_no_provider_for_space_in_oz(
    client,
    user,
    providers_list,
    space_name,
    host,
    selenium,
    oz_page,
    users,
    hosts,
    spaces,
    admin_credentials,
):

    if client.lower() == "rest":

        assert_there_is_no_provider_for_space_in_oz_rest(
            user,
            users,
            host,
            hosts,
            space_name,
            spaces,
            providers_list,
            admin_credentials,
        )
    elif client.lower() == "web gui":

        assert_there_is_no_provider_for_space_in_oz_gui(
            selenium, user, oz_page, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that "
        "(?P<user_list>.+?) (is|are) members? of "
        '"(?P<space_name>.+?)" in "(?P<host>.+?)" Onezone service'
    )
)
def assert_user_is_member_of_space(
    client,
    user,
    user_list,
    space_name,
    host,
    spaces,
    users,
    hosts,
    selenium,
    oz_page,
    onepanel,
):

    if client.lower() == "rest":

        assert_user_is_member_of_space_rest(
            space_name, spaces, user, users, user_list, host, hosts
        )
    elif client.lower() == "web gui":

        assert_user_is_member_of_space_gui(
            selenium, user, space_name, oz_page, user_list, onepanel
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees provider "
        '"(?P<provider_name>.+?)" with hostname matches that of '
        '"(?P<provider>.+?)" provider in "(?P<host>.+?)" Onezone '
        "service"
    )
)
def assert_provider_has_given_name_and_known_hostname_in_oz(
    client,
    user,
    provider_name,
    provider,
    host,
    users,
    hosts,
    selenium,
    oz_page,
    popups,
):

    provider_name = hosts[provider_name]["name"]

    if client.lower() == "rest":

        assert_provider_has_name_and_hostname_in_oz_rest(
            user, users, host, hosts, provider_name, hosts[provider]["hostname"]
        )
    elif client.lower() == "web gui":

        assert_provider_has_name_and_hostname_in_oz_gui(
            selenium, user, oz_page, provider_name, provider, hosts, popups
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")
