"""This module contains gherkin steps to run mixed acceptance tests featuring
datasets using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.conftest import WAIT_FRONTEND
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
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) creates dataset "
        '(?P<option>.*)for item "(?P<item_name>.*)" in space '
        '"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_dataset_in_op(
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
    option,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        create_dataset(
            user,
            tmp_memory,
            item_name,
            space_name,
            selenium,
            oz_page,
            op_container,
            modals,
            popups,
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
        "using (?P<client>.*), (?P<user>.+?) fails to create dataset for"
        ' item "(?P<item_name>.*)" in space '
        '"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_create_dataset_in_op(
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
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        fail_to_create_dataset_in_op_gui(
            user,
            tmp_memory,
            item_name,
            space_name,
            selenium,
            oz_page,
            op_container,
            modals,
            popups,
        )
    elif client_lower == "rest":
        fail_to_create_dataset_in_op_rest(
            user, users, hosts, host, space_name, item_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) (?P<option>does "
        'not see|sees) dataset for item "(?P<item_name>.*)" in space'
        ' "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_top_level_dataset_in_space_in_op(
    client,
    user,
    item_name,
    space_name,
    host,
    selenium,
    oz_page,
    op_container,
    tmp_memory,
    users,
    hosts,
    spaces,
    option,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_top_level_dataset_in_space_in_op_gui(
            selenium,
            user,
            oz_page,
            space_name,
            op_container,
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
        "using (?P<client>.*), (?P<user>.+?) removes dataset for item "
        '"(?P<item_name>.*)" in space "(?P<space_name>.*)" '
        "in (?P<host>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_dataset_in_op(
    client,
    user,
    item_name,
    space_name,
    host,
    selenium,
    oz_page,
    op_container,
    tmp_memory,
    modals,
    users,
    hosts,
    spaces,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        remove_dataset_in_op_gui(
            selenium,
            user,
            oz_page,
            space_name,
            op_container,
            tmp_memory,
            item_name,
            modals,
            popups,
        )
    elif client_lower == "rest":
        remove_dataset_in_op_rest(
            user, users, hosts, host, space_name, item_name, spaces
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees (?P<option>.*) write "
        'protection flags? for dataset for item "(?P<item_name>.*)" in'
        ' space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_write_protection_flag_for_dataset(
    client,
    user,
    item_name,
    option,
    tmp_memory,
    users,
    hosts,
    host,
    space_name,
    spaces,
):
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
        "using (?P<client>.*), (?P<user>.+?) sees that datasets "
        'structure in space "(?P<space_name>.*)" in (?P<host>.*) '
        r"is as follow:\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_dataset_structure_in_op(
    client,
    user,
    space_name,
    host,
    config,
    selenium,
    oz_page,
    op_container,
    tmpdir,
    tmp_memory,
    users,
    hosts,
    spaces,
):
    # function checks only if what is in config exists, does not
    # fail if there are more datasets
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_space_content_in_op_gui(
            config,
            selenium,
            user,
            op_container,
            tmp_memory,
            tmpdir,
            space_name,
            oz_page,
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
        "using (?P<client>.*), (?P<user>.+?) sees that item"
        ' "(?P<item_name>.*)" has effective(?P<option>.*) '
        'write protection flags? in space "(?P<space_name>.*)" '
        "in (?P<host>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_effective_protection_flags_for_file(
    client,
    user,
    item_name,
    option,
    space_name,
    host,
    selenium,
    oz_page,
    op_container,
    tmp_memory,
    modals,
    users,
    hosts,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        check_effective_protection_flags_for_file_in_op_gui(
            selenium,
            user,
            oz_page,
            space_name,
            op_container,
            tmp_memory,
            item_name,
            modals,
            option,
            popups,
        )

    elif client_lower == "rest":
        check_effective_protection_flags_for_file_in_op_rest(
            user, users, hosts, host, item_name, option, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sets(?P<option>.*) "
        'protection flags? for dataset "(?P<item_name>.*)" in space '
        '"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def set_protection_flags_for_dataset(
    client,
    user,
    option,
    item_name,
    space_name,
    host,
    selenium,
    oz_page,
    op_container,
    tmp_memory,
    modals,
    users,
    hosts,
    spaces,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        set_protection_flags_for_dataset_in_op_gui(
            user,
            selenium,
            oz_page,
            space_name,
            op_container,
            tmp_memory,
            item_name,
            modals,
            option,
            popups,
        )

    elif client_lower == "rest":
        set_protection_flags_for_dataset_in_op_rest(
            user, users, hosts, host, item_name, option, spaces, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that dataset"
        ' "(?P<item_name>.*)" has effective(?P<option>.*) '
        'write protection flags? in space "(?P<space_name>.*)" '
        "in (?P<host>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_effective_protection_flags_for_dataset(
    client,
    user,
    item_name,
    option,
    space_name,
    host,
    selenium,
    oz_page,
    op_container,
    tmp_memory,
    modals,
    users,
    hosts,
    spaces,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        check_effective_protection_flags_for_file_in_op_gui(
            selenium,
            user,
            oz_page,
            space_name,
            op_container,
            tmp_memory,
            item_name,
            modals,
            option,
            popups,
        )
    elif client_lower == "rest":
        check_effective_protection_flags_for_dataset_in_op_rest(
            user, users, hosts, host, item_name, option, spaces, space_name
        )

    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) detaches dataset "
        'for item "(?P<item_name>.*)" in space "(?P<space_name>.*)" '
        "in (?P<host>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def detach_dataset_in_op(
    client,
    user,
    selenium,
    space_name,
    op_container,
    tmp_memory,
    item_name,
    modals,
    oz_page,
    users,
    hosts,
    host,
    spaces,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        detach_dataset_in_op_gui(
            selenium,
            user,
            oz_page,
            space_name,
            op_container,
            tmp_memory,
            item_name,
            modals,
            popups,
        )
    elif client_lower == "rest":
        detach_dataset_in_op_rest(
            user, users, hosts, host, item_name, spaces, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that dataset for item"
        ' "(?P<item_name>.*)" is detached in space "(?P<space_name>.*)"'
        " in (?P<host>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_dataset_detached_in_op(
    client,
    selenium,
    user,
    oz_page,
    space_name,
    op_container,
    tmp_memory,
    item_name,
    users,
    hosts,
    host,
    spaces,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_dataset_detached_in_op_gui(
            selenium,
            user,
            oz_page,
            item_name,
            space_name,
            op_container,
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
        "using (?P<client>.*), (?P<user>.+?) reattaches dataset for "
        'item "(?P<item_name>.*)" in space "(?P<space_name>.*)" '
        "in (?P<host>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def reattach_dataset_in_op(
    client,
    user,
    selenium,
    space_name,
    op_container,
    tmp_memory,
    item_name,
    modals,
    oz_page,
    users,
    hosts,
    host,
    spaces,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        reattach_dataset_in_op_gui(
            selenium,
            user,
            oz_page,
            space_name,
            op_container,
            tmp_memory,
            item_name,
            modals,
            popups,
        )
    elif client_lower == "rest":
        reattach_dataset_in_op_rest(
            user, users, hosts, host, item_name, spaces, space_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")
