"""This module contains definitions of fixtures used in oneclient tests
of onedata.
"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

import pytest
from tests.conftest import export_logs
from tests.oneclient.steps.multi_dir_steps import purge_all_spaces
from tests.utils.entities_setup.groups import groups_creation as setup_groups
from tests.utils.entities_setup.spaces import (
    create_and_configure_spaces as setup_spaces,
)
from tests.utils.entities_setup.users import (
    users_creation_with_cleanup as setup_users,
)
from tests.utils.luma_utils import (
    add_spaces_luma_mapping,
    add_user_luma_mapping,
    get_all_spaces_details,
    get_local_feed_luma_storages,
)


@pytest.fixture(autouse=True)
def skip_by_env(skip_by_env):
    """Autouse fixture defined in tests.conftest"""


@pytest.fixture(autouse=True)
def xfail_by_env(xfail_by_env):
    """Autouse fixture defined in tests.conftest"""


@pytest.fixture(autouse=True, scope="module")
def run_around_suite(request, env_description_abs_path):
    yield
    export_logs(request, env_description_abs_path)


@pytest.fixture(autouse=True)
def run_around_testcase(
    entities_config,
    admin_credentials,
    onepanel_credentials,
    hosts,
    users,
    groups,
    storages,
    spaces,
    rm_users,
):
    unmount_all_clients_and_purge_spaces(users)
    setup_entities(
        entities_config,
        admin_credentials,
        onepanel_credentials,
        hosts,
        users,
        groups,
        storages,
        spaces,
        rm_users,
    )
    yield
    unmount_all_clients_and_purge_spaces(users)


def setup_entities(
    config,
    admin_credentials,
    onepanel_credentials,
    hosts,
    users,
    groups,
    storages,
    spaces,
    rm_users,
):
    setup_users(
        "onezone",
        config.get("users"),
        admin_credentials,
        onepanel_credentials,
        hosts,
        users,
        rm_users,
    )
    setup_groups(
        config.get("groups"), "onezone", admin_credentials, users, hosts, groups
    )
    setup_spaces(
        config.get("spaces"),
        "onezone",
        admin_credentials,
        onepanel_credentials,
        hosts,
        users,
        groups,
        storages,
        spaces,
    )
    setup_luma(config.get("users"), users, admin_credentials, hosts)


def setup_luma(users_config, users, admin_credentials, hosts):
    spaces = get_all_spaces_details(admin_credentials, hosts)
    local_feed_luma_storages = get_local_feed_luma_storages(
        admin_credentials, hosts
    )

    for username in users_config:
        new_user = users[username]
        add_user_luma_mapping(
            admin_credentials, new_user, local_feed_luma_storages
        )

    add_spaces_luma_mapping(admin_credentials, local_feed_luma_storages, spaces)


def unmount_all_clients_and_purge_spaces(users):
    for user in users.values():
        for client in user.clients.values():
            purge_spaces(client)
            client.unmount()
        user.clients.clear()


def purge_spaces(client):
    purge_all_spaces(client)


def pytest_bdd_before_scenario(request, feature, scenario):
    print(
        "\n================================================================="
    )
    print(f"- Executing scenario '{scenario.name}'")
    print(f"- from feature '{feature.name}'")
    print("-----------------------------------------------------------------")


def pytest_bdd_before_step_call(
    request, feature, scenario, step, step_func, step_func_args
):
    print(f"-- Executing step: '{step}'")


def pytest_bdd_step_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    print("--- STEP FAILED\n")


def pytest_bdd_after_scenario(request, feature, scenario):
    print(
        "=================================================================\n"
    )
