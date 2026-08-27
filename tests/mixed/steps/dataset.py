"""This module contains gherkin steps to run mixed acceptance tests featuring
datasets using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Mapping

from _pytest._py.path import LocalPath

from tests.gui.meta_steps.oneprovider.data import assert_space_content_in_op_gui
from tests.gui.meta_steps.oneprovider.dataset import (
    assert_dataset_detached_in_op_gui,
    assert_top_level_dataset_in_space_in_op_gui,
    check_effective_protection_flags_for_file_in_op_gui,
    create_dataset,
    detach_dataset_in_op_gui,
    fail_to_create_dataset_in_op_gui,
    reattach_dataset_in_op_gui,
    remove_dataset_in_op_gui,
    set_protection_flags_for_dataset_in_op_gui,
)
from tests.gui.steps.oneprovider.browser import assert_status_tag_for_file_in_browser
from tests.gui.steps.onezone.spaces import click_on_option_of_space_on_left_sidebar_menu
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils.common.constants import WAIT_FRONTEND
from tests.mixed.steps.rest.oneprovider.datasets import (
    assert_dataset_detached_in_op_rest,
    assert_top_level_dataset_in_space_in_op_rest,
    assert_write_protection_flag_for_dataset_op_rest,
    check_dataset_structure_in_op_rest,
    check_effective_protection_flags_for_dataset_in_op_rest,
    check_effective_protection_flags_for_file_in_op_rest,
    create_dataset_in_op_rest,
    detach_dataset_in_op_rest,
    fail_to_create_dataset_in_op_rest,
    get_flags,
    reattach_dataset_in_op_rest,
    remove_dataset_in_op_rest,
    set_protection_flags_for_dataset_in_op_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        r"using (?P<client>.*), (user of )?(?P<user>.+?) creates dataset "
        r'(?P<option>.*)for item "(?P<item_name>.*)" in space '
        r'"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_dataset_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    option: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        create_dataset(
            user,
            tmp_memory,
            item_name,
            space_name,
            selenium,
            option=option,
        )
    elif client_lower == "rest":
        create_dataset_in_op_rest(
            user, users, hosts, host, space_name, item_name, option
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) fails to create dataset for"
        r' item "(?P<item_name>.*)" in space '
        r'"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_create_dataset_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        fail_to_create_dataset_in_op_gui(
            user,
            tmp_memory,
            item_name,
            space_name,
            selenium,
        )
    elif client_lower == "rest":
        fail_to_create_dataset_in_op_rest(
            user, users, hosts, host, space_name, item_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) (?P<option>does "
        r'not see|sees) dataset for item "(?P<item_name>.*)" in space'
        r' "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_top_level_dataset_in_space_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
    option: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_top_level_dataset_in_space_in_op_gui(
            selenium,
            user,
            space_name,
            tmp_memory,
            item_name,
            option,
        )
    elif client_lower == "rest":
        assert_top_level_dataset_in_space_in_op_rest(
            user, users, hosts, host, space_name, item_name, spaces, option
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) removes dataset for item "
        r'"(?P<item_name>.*)" in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_dataset_in_op(
    client: str,
    user: str,
    item_name: str,
    space_name: str,
    host: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        remove_dataset_in_op_gui(
            selenium,
            user,
            space_name,
            tmp_memory,
            item_name,
        )
    elif client_lower == "rest":
        remove_dataset_in_op_rest(
            user, users, hosts, host, space_name, item_name, spaces
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees (?P<option>.*) write "
        r'protection flags? for dataset for item "(?P<item_name>.*)" in'
        r' space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_write_protection_flag_for_dataset(
    client: str,
    user: str,
    item_name: str,
    option: str,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    host: str,
    space_name: str,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        flags = [
            item.replace("_protection", "_protected") for item in get_flags(option)
        ]
        for flag in flags:
            assert_status_tag_for_file_in_browser(
                user,
                flag,
                item_name,
                tmp_memory,
                which_browser="dataset browser",
            )
    elif client_lower == "rest":
        assert_write_protection_flag_for_dataset_op_rest(
            user, users, hosts, host, space_name, item_name, spaces, option
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that datasets "
        r'structure in space "(?P<space_name>.*)" in (?P<host>.*) '
        r"is as follow:\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_dataset_structure_in_op(
    client: str,
    user: str,
    space_name: str,
    host: str,
    config: str,
    selenium: SeleniumDrivers,
    tmpdir: LocalPath,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
) -> None:
    # function checks only if what is in config exists, does not
    # fail if there are more datasets
    client_lower = client.lower()
    if client_lower == "web gui":
        option_in_submenu = "datasets, archives"
        click_on_option_of_space_on_left_sidebar_menu(
            selenium, user, space_name, option_in_submenu
        )
        assert_space_content_in_op_gui(
            config,
            selenium,
            user,
            tmp_memory,
            tmpdir,
            space_name,
            which_browser="dataset browser",
        )
    elif client_lower == "rest":
        check_dataset_structure_in_op_rest(
            user, users, hosts, host, spaces, space_name, config
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that item"
        r' "(?P<item_name>.*)" has effective(?P<option>.*) '
        r'write protection flags? in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_effective_protection_flags_for_file(
    client: str,
    user: str,
    item_name: str,
    option: str,
    space_name: str,
    host: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        check_effective_protection_flags_for_file_in_op_gui(
            selenium,
            user,
            space_name,
            tmp_memory,
            item_name,
            option,
        )

    elif client_lower == "rest":
        check_effective_protection_flags_for_file_in_op_rest(
            user, users, hosts, host, item_name, option, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sets(?P<option>.*) "
        r'protection flags? for dataset "(?P<item_name>.*)" in space '
        r'"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def set_protection_flags_for_dataset(
    client: str,
    user: str,
    option: str,
    item_name: str,
    space_name: str,
    host: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        set_protection_flags_for_dataset_in_op_gui(
            user,
            selenium,
            space_name,
            tmp_memory,
            item_name,
            option,
        )

    elif client_lower == "rest":
        set_protection_flags_for_dataset_in_op_rest(
            user, users, hosts, host, item_name, option, spaces, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that dataset"
        r' "(?P<item_name>.*)" has effective(?P<option>.*) '
        r'write protection flags? in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_effective_protection_flags_for_dataset(
    client: str,
    user: str,
    item_name: str,
    option: str,
    space_name: str,
    host: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        check_effective_protection_flags_for_file_in_op_gui(
            selenium,
            user,
            space_name,
            tmp_memory,
            item_name,
            option,
        )
    elif client_lower == "rest":
        check_effective_protection_flags_for_dataset_in_op_rest(
            user, users, hosts, host, item_name, option, spaces, space_name
        )

    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) detaches dataset "
        r'for item "(?P<item_name>.*)" in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def detach_dataset_in_op(
    client: str,
    user: str,
    selenium: SeleniumDrivers,
    space_name: str,
    tmp_memory: TmpMemory,
    item_name: str,
    users: Users,
    hosts: Hosts,
    host: str,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        detach_dataset_in_op_gui(
            selenium,
            user,
            space_name,
            tmp_memory,
            item_name,
        )
    elif client_lower == "rest":
        detach_dataset_in_op_rest(
            user, users, hosts, host, item_name, spaces, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) sees that dataset for item"
        r' "(?P<item_name>.*)" is detached in space '
        r'"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_dataset_detached_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    tmp_memory: TmpMemory,
    item_name: str,
    users: Users,
    hosts: Hosts,
    host: str,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_dataset_detached_in_op_gui(
            selenium,
            user,
            item_name,
            space_name,
            tmp_memory,
        )
    elif client_lower == "rest":
        assert_dataset_detached_in_op_rest(
            user, users, hosts, host, item_name, spaces, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>.+?) reattaches dataset for "
        r'item "(?P<item_name>.*)" in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def reattach_dataset_in_op(
    client: str,
    user: str,
    selenium: SeleniumDrivers,
    space_name: str,
    tmp_memory: TmpMemory,
    item_name: str,
    users: Users,
    hosts: Hosts,
    host: str,
    spaces: Mapping[str, str],
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        reattach_dataset_in_op_gui(
            selenium,
            user,
            space_name,
            tmp_memory,
            item_name,
        )
    elif client_lower == "rest":
        reattach_dataset_in_op_rest(
            user, users, hosts, host, item_name, spaces, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")
