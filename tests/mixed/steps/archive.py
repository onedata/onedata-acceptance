"""This module contains gherkin steps to run mixed acceptance tests featuring
archives using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Mapping
from typing import cast

import yaml

from tests.gui.constants import WAIT_FRONTEND
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
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.mixed.steps.rest.oneprovider.archives import (
    assert_archive_callback_in_op_rest,
    assert_archive_in_op_rest,
    assert_archive_with_option_in_op_rest,
    assert_base_archive_for_archive_in_op_rest,
    assert_number_of_archive_in_op_rest,
    assert_progress_of_recall_in_op_rest,
    cancel_archive_for_archive_in_op_rest,
    create_archive_in_op_rest,
    create_n_archives_in_op_rest,
    recall_archive_for_archive_in_op_rest,
    recalled_archive_details_in_op_rest,
    remove_archive_in_op_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) "
        r"(?P<option>succeeds|fails|tries)"
        r' to create archive for item "(?P<item_name>.*)" in space'
        r' "(?P<space_name>.*)" in (?P<host>.*) with following '
        r"configuration:\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_archive_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    config: str,
    spaces: Mapping[str, str],
    clipboard: Clipboard,
    displays: dict[str, str],
    option: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        create_archive(
            user,
            selenium,
            config,
            item_name,
            space_name,
            tmp_memory,
            clipboard,
            displays,
            option,
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
    parsers.parse(
        'using REST, {user} creates {number} archives for dataset "{item_name}" in '
        'space "{space_name}" in host {host} with following configuration:\n{config}'
    )
)
def wt_create_n_archives_in_op(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    space_name: str,
    item_name: str,
    config: str,
    spaces: Mapping[str, str],
    tmp_memory: TmpMemory,
    number: str,
) -> None:
    create_n_archives_in_op_rest(
        user,
        users,
        hosts,
        host,
        space_name,
        item_name,
        config,
        spaces,
        tmp_memory,
        int(number),
    )


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) (?P<option>does not "
        r'see|sees) archive with description: "(?P<description>.*)" for'
        r' item "(?P<item_name>.*)" in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
    option: str,
    description: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_archive_in_op_gui(
            user,
            selenium,
            item_name,
            space_name,
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
        r"using (?P<client>.*), (?P<user>.+?) (?P<option>succeeds|fails) "
        r'to remove archive with description: "(?P<description>.*)" '
        r'for item "(?P<item_name>.*)" in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_archive_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    description: str,
    option: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        remove_archive_in_op_gui(
            user,
            selenium,
            item_name,
            space_name,
            tmp_memory,
            description,
            option,
        )
    elif client_lower == "rest":
        remove_archive_in_op_rest(
            user, users, hosts, host, description, tmp_memory, option
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees (?P<option>.*) "
        r'archive with description: "(?P<description>.*)" for dataset '
        r'for item "(?P<item_name>.*)" in space '
        r'"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_with_option_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    option: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    description: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_archive_with_option_in_op_gui(
            user,
            selenium,
            space_name,
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
        r"using (?P<client>.*), (?P<user>.+?) sees that dataset for"
        r' item "(?P<item_name>.*)" has (?P<number>.*) archive in '
        r'space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_archive_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
    number: str,
) -> None:
    expected_number = int(number)
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_number_of_archive_in_op_gui(
            user,
            selenium,
            item_name,
            space_name,
            tmp_memory,
            expected_number,
        )
    elif client_lower == "rest":
        assert_number_of_archive_in_op_rest(
            user, users, hosts, host, space_name, item_name, spaces, expected_number
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that archive with "
        r'description "(?P<description>.*)" has base archive with '
        r'description "(?P<base_description>.*)" for item '
        r'"(?P<item_name>.*)" in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_base_archive_for_archive_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    description: str,
    base_description: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_base_archive_for_archive_in_op_gui(
            user,
            selenium,
            item_name,
            space_name,
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
        r"using (?P<client>.*), (?P<user>.+?) sees that (?P<option>.*) "
        r'callback is "(?P<expected_callback>.*)" for archive with '
        r'description "(?P<description>.*)" for item "(?P<item_name>.*)"'
        r' in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_callback(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    description: str,
    option: str,
    expected_callback: str,
    client: str,
    selenium: SeleniumDrivers,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_archive_callback_in_op_gui(
            user,
            tmp_memory,
            description,
            selenium,
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
        r"using (?P<client>.*), (?P<user>.+?) recalls archive with "
        r'description "(?P<description>.*)" into "(?P<item_name>.*)" '
        r'parent directory with target name "(?P<target_name>.*)" in '
        r'space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
def recall_archive_for_archive_in_op(
    client: str,
    user: str,
    description: str,
    target_name: str,
    space_name: str,
    host: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
) -> None:

    client_lower = client.lower()
    if client_lower == "web gui":
        recall_archive_for_archive_in_op_gui(
            user, description, tmp_memory, selenium, target_name
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
        r'using (?P<client>.*), (?P<user>.+?) checks "(?P<name>.*)" '
        r'archive recalled details in "(?P<space_name>.*)" in'
        r" (?P<host>.*) and sees following:\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def recall_archive_details_in_op(
    client: str,
    user: str,
    config: str,
    name: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    host: str,
    space_name: str,
    spaces: Mapping[str, str],
) -> None:

    client_lower = client.lower()
    data = cast(dict[str, str], yaml.load(config, yaml.Loader))
    if client_lower == "web gui":
        recalled_archive_details_in_op_gui(user, name, tmp_memory, data, selenium)
    elif client_lower == "rest":
        recalled_archive_details_in_op_rest(
            user, users, hosts, host, data, name, space_name, spaces
        )

    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.+?), (?P<user>.+?) sees progress of archive "
        r'recall for "(?P<name>.*)" in "(?P<space_name>.*)" in'
        r" (?P<host>.*):\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_progress_of_recall_in_op(
    user: str,
    name: str,
    client: str,
    space_name: str,
    host: str,
    hosts: Hosts,
    users: Users,
    config: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "rest":
        assert_progress_of_recall_in_op_rest(
            user, name, space_name, host, hosts, users, config
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.+?), (?P<user>.+?) cancels archive "
        r'recall for "(?P<target_name>.*)" for archive with description'
        r' "(?P<description>.*)" for item "(?P<name>.*)" in space'
        r' "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def cancel_archive_for_archive_in_op(
    client: str,
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    space_name: str,
    target_name: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "rest":
        cancel_archive_for_archive_in_op_rest(
            user, users, hosts, host, space_name, target_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")
