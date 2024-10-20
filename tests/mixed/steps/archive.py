"""This module contains gherkin steps to run mixed acceptance tests featuring
archives using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import yaml
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.archives import (
    assert_archive_callback_in_op_gui,
    assert_archive_in_op_gui,
    assert_archive_with_option_in_op_gui,
    assert_base_archive_for_archive_in_op_gui,
    assert_number_of_archive_in_op_gui,
    create_archive,
    recall_archive_for_archive_in_op_gui,
    recalled_archive_details_in_op_gui,
    remove_archive_in_op_gui,
)
from tests.mixed.steps.rest.oneprovider.archives import (
    assert_archive_callback_in_op_rest,
    assert_archive_in_op_rest,
    assert_archive_with_option_in_op_rest,
    assert_base_archive_for_archive_in_op_rest,
    assert_number_of_archive_in_op_rest,
    assert_progress_of_recall_in_op_rest,
    cancel_archive_for_archive_in_op_rest,
    create_archive_in_op_rest,
    recall_archive_for_archive_in_op_rest,
    recalled_archive_details_in_op_rest,
    remove_archive_in_op_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) "
        "(?P<option>succeeds|fails|tries)"
        ' to create archive for item "(?P<item_name>.*)" in space'
        ' "(?P<space_name>.*)" in (?P<host>.*) with following '
        r"configuration:\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_archive_in_op(
    client,
    user,
    item_name,
    space_name,
    host,
    tmp_memory,
    selenium,
    oz_page,
    op_container,
    modals,
    users,
    hosts,
    config,
    spaces,
    clipboard,
    displays,
    option,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        create_archive(
            user,
            selenium,
            config,
            item_name,
            space_name,
            oz_page,
            op_container,
            tmp_memory,
            modals,
            clipboard,
            displays,
            option,
            popups,
        )
    elif client_lower == "rest":
        create_archive_in_op_rest(
            user,
            users,
            hosts,
            host,
            space_name,
            item_name,
            config,
            spaces,
            tmp_memory,
            option,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) (?P<option>does not "
        'see|sees) archive with description: "(?P<description>.*)" for'
        ' item "(?P<item_name>.*)" in space "(?P<space_name>.*)" '
        "in (?P<host>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_in_op(
    client,
    user,
    item_name,
    space_name,
    host,
    tmp_memory,
    selenium,
    oz_page,
    op_container,
    users,
    hosts,
    spaces,
    option,
    description,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_archive_in_op_gui(
            user,
            selenium,
            item_name,
            space_name,
            oz_page,
            op_container,
            tmp_memory,
            option,
            description,
        )
    elif client_lower == "rest":
        assert_archive_in_op_rest(
            user,
            users,
            hosts,
            host,
            space_name,
            item_name,
            spaces,
            tmp_memory,
            option,
            description,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) (?P<option>succeeds|fails) "
        'to remove archive with description: "(?P<description>.*)" '
        'for item "(?P<item_name>.*)" in space "(?P<space_name>.*)" '
        "in (?P<host>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_archive_in_op(
    client,
    user,
    item_name,
    space_name,
    host,
    tmp_memory,
    selenium,
    oz_page,
    op_container,
    users,
    hosts,
    modals,
    description,
    option,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        remove_archive_in_op_gui(
            user,
            selenium,
            item_name,
            space_name,
            oz_page,
            op_container,
            tmp_memory,
            modals,
            description,
            option,
            popups,
        )
    elif client_lower == "rest":
        remove_archive_in_op_rest(
            user, users, hosts, host, description, tmp_memory, option
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees (?P<option>.*) "
        'archive with description: "(?P<description>.*)" for dataset '
        'for item "(?P<item_name>.*)" in space '
        '"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_with_option_in_op(
    client,
    user,
    item_name,
    space_name,
    host,
    option,
    selenium,
    oz_page,
    op_container,
    tmp_memory,
    users,
    hosts,
    description,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_archive_with_option_in_op_gui(
            user,
            selenium,
            oz_page,
            space_name,
            op_container,
            tmp_memory,
            item_name,
            option,
            description,
        )
    elif client_lower == "rest":
        assert_archive_with_option_in_op_rest(
            user, users, hosts, host, option, tmp_memory, description
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that dataset for"
        ' item "(?P<item_name>.*)" has (?P<number>.*) archive in '
        'space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_archive_in_op(
    client,
    user,
    item_name,
    space_name,
    host,
    tmp_memory,
    selenium,
    oz_page,
    op_container,
    users,
    hosts,
    spaces,
    number,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_number_of_archive_in_op_gui(
            user,
            selenium,
            item_name,
            space_name,
            oz_page,
            op_container,
            tmp_memory,
            number,
        )
    elif client_lower == "rest":
        assert_number_of_archive_in_op_rest(
            user, users, hosts, host, space_name, item_name, spaces, number
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that archive with "
        'description "(?P<description>.*)" has base archive with '
        'description "(?P<base_description>.*)" for item '
        '"(?P<item_name>.*)" in space "(?P<space_name>.*)" in'
        " (?P<host>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_base_archive_for_archive_in_op(
    client,
    user,
    item_name,
    space_name,
    host,
    description,
    base_description,
    selenium,
    oz_page,
    op_container,
    tmp_memory,
    users,
    hosts,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_base_archive_for_archive_in_op_gui(
            user,
            selenium,
            item_name,
            space_name,
            oz_page,
            op_container,
            tmp_memory,
            description,
            base_description,
        )
    elif client_lower == "rest":
        assert_base_archive_for_archive_in_op_rest(
            user, users, hosts, host, tmp_memory, description, base_description
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that (?P<option>.*) "
        'callback is "(?P<expected_callback>.*)" for archive with '
        'description "(?P<description>.*)" for item "(?P<item_name>.*)"'
        ' in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_callback(
    user,
    users,
    hosts,
    host,
    tmp_memory,
    description,
    option,
    expected_callback,
    client,
    selenium,
    popups,
    modals,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_archive_callback_in_op_gui(
            user,
            tmp_memory,
            description,
            selenium,
            popups,
            modals,
            expected_callback,
            option,
        )
    elif client_lower == "rest":
        assert_archive_callback_in_op_rest(
            user,
            users,
            hosts,
            host,
            tmp_memory,
            description,
            option,
            expected_callback,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) recalls archive with "
        'description "(?P<description>.*)" into "(?P<item_name>.*)" '
        'parent directory with target name "(?P<target_name>.*)" in '
        'space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
def recall_archive_for_archive_in_op(
    client,
    user,
    description,
    target_name,
    space_name,
    host,
    tmp_memory,
    popups,
    selenium,
    modals,
    users,
    hosts,
    spaces,
):

    client_lower = client.lower()
    if client_lower == "web gui":
        recall_archive_for_archive_in_op_gui(
            user, description, tmp_memory, popups, selenium, modals, target_name
        )
    elif client_lower == "rest":
        recall_archive_for_archive_in_op_rest(
            user,
            users,
            hosts,
            host,
            tmp_memory,
            description,
            target_name,
            space_name,
            spaces,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        'using (?P<client>.*), (?P<user>.+?) checks "(?P<name>.*)" '
        r'archive recalled details in "(?P<space_name>.*)" in'
        r" (?P<host>.*) and sees following:\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def recall_archive_details_in_op(
    client,
    user,
    config,
    name,
    tmp_memory,
    modals,
    selenium,
    users,
    hosts,
    host,
    space_name,
    spaces,
):

    client_lower = client.lower()
    data = yaml.load(config, yaml.Loader)
    if client_lower == "web gui":
        recalled_archive_details_in_op_gui(
            user, name, tmp_memory, data, modals, selenium
        )
    elif client_lower == "rest":
        recalled_archive_details_in_op_rest(
            user, users, hosts, host, data, name, space_name, spaces
        )

    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.+?), (?P<user>.+?) sees progress of archive "
        'recall for "(?P<name>.*)" in "(?P<space_name>.*)" in'
        r" (?P<host>.*):\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_progress_of_recall_in_op(
    user, name, client, space_name, host, hosts, users, config
):
    client_lower = client.lower()
    if client_lower == "rest":
        assert_progress_of_recall_in_op_rest(
            user, name, space_name, host, hosts, users, config
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.+?), (?P<user>.+?) cancels archive "
        'recall for "(?P<target_name>.*)" for archive with description'
        ' "(?P<description>.*)" for item "(?P<name>.*)" in space'
        ' "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def cancel_archive_for_archive_in_op(
    client, user, users, hosts, host, space_name, target_name
):
    client_lower = client.lower()
    if client_lower == "rest":
        cancel_archive_for_archive_in_op_rest(
            user, users, hosts, host, space_name, target_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")
