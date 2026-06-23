"""This module contains definitions of fixtures used in oneclient tests
of onedata.
"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Callable, Generator, Mapping
from typing import Protocol, cast

import pytest

from tests.conftest import Hosts, Storages, TestConfig, Users, export_logs
from tests.oneclient.steps.multi_dir_steps import purge_all_spaces
from tests.utils.client_utils import Client
from tests.utils.entities_setup.groups import CredentialsLike, GroupsConfig, UserLike
from tests.utils.entities_setup.groups import groups_creation as setup_groups
from tests.utils.entities_setup.spaces import (
    SpacesConfig,
)
from tests.utils.entities_setup.spaces import (
    create_and_configure_spaces as setup_spaces,
)
from tests.utils.entities_setup.users import UserConfigEntry, UsersDb
from tests.utils.entities_setup.users import users_creation_with_cleanup as setup_users
from tests.utils.luma_utils import (
    add_spaces_luma_mapping,
    add_user_luma_mapping,
    get_all_spaces_details,
    get_local_feed_luma_storages,
)
from tests.utils.user_utils import AdminUser


class HasName(Protocol):
    name: str


@pytest.fixture(autouse=True)
def skip_by_env(skip_by_env: object) -> None:
    """Autouse fixture defined in tests.conftest"""


@pytest.fixture(autouse=True)
def xfail_by_env(xfail_by_env: object) -> None:
    """Autouse fixture defined in tests.conftest"""


@pytest.fixture(autouse=True, scope="module")
def run_around_suite(
    request: pytest.FixtureRequest, env_description_abs_path: str
) -> Generator[None, None, None]:
    yield
    export_logs(request, env_description_abs_path)


@pytest.fixture(autouse=True)
def run_around_testcase(
    entities_config: TestConfig,
    admin_credentials: AdminUser,
    onepanel_credentials: AdminUser,
    hosts: Hosts,
    users: Users,
    groups: dict[str, str],
    storages: Storages,
    spaces: dict[str, str],
    rm_users: bool,
) -> Generator[None, None, None]:
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
    config: TestConfig,
    admin_credentials: AdminUser,
    onepanel_credentials: AdminUser,
    hosts: Hosts,
    users: Users,
    groups: dict[str, str],
    storages: Storages,
    spaces: dict[str, str],
    rm_users: bool,
) -> None:
    setup_users(
        "onezone",
        cast(list[UserConfigEntry], config.get("users")),
        cast(CredentialsLike, admin_credentials),
        cast(CredentialsLike, onepanel_credentials),
        cast(Mapping[str, Mapping[str, str]], hosts),
        cast(UsersDb, users),
        rm_users,
    )
    setup_groups(
        cast(GroupsConfig, config.get("groups")),
        "onezone",
        cast(CredentialsLike, admin_credentials),
        cast(Mapping[str, UserLike], users),
        cast(Mapping[str, Mapping[str, str]], hosts),
        groups,
    )
    setup_spaces(
        cast(SpacesConfig, config.get("spaces")),
        "onezone",
        admin_credentials,
        onepanel_credentials,
        hosts,
        users,
        groups,
        storages,
        spaces,
    )
    setup_luma(
        cast(list[UserConfigEntry], config.get("users")),
        users,
        admin_credentials,
        hosts,
    )


def setup_luma(
    users_config: list[UserConfigEntry],
    users: Users,
    admin_credentials: AdminUser,
    hosts: Hosts,
) -> None:
    hosts_config = cast(Mapping[str, Mapping[str, str]], hosts)
    spaces = get_all_spaces_details(admin_credentials, hosts_config)
    local_feed_luma_storages = get_local_feed_luma_storages(
        admin_credentials, hosts_config
    )

    for user_config in users_config:
        username = (
            user_config if isinstance(user_config, str) else next(iter(user_config))
        )
        new_user = users[username]
        add_user_luma_mapping(admin_credentials, new_user, local_feed_luma_storages)

    add_spaces_luma_mapping(admin_credentials, local_feed_luma_storages, spaces)


def unmount_all_clients_and_purge_spaces(users: Users) -> None:
    for user in users.values():
        for client in user.clients.values():
            purge_spaces(client)
            client.unmount()
        user.clients.clear()


def purge_spaces(client: Client) -> None:
    purge_all_spaces(client)


def pytest_bdd_before_scenario(
    request: pytest.FixtureRequest, feature: HasName, scenario: HasName
) -> None:
    print("\n=================================================================")
    print(f"- Executing scenario '{scenario.name}'")
    print(f"- from feature '{feature.name}'")
    print("-----------------------------------------------------------------")


def pytest_bdd_before_step_call(
    request: pytest.FixtureRequest,
    feature: object,
    scenario: object,
    step: object,
    step_func: Callable[..., object],
    step_func_args: dict[str, object],
) -> None:
    print(f"-- Executing step: '{step}'")


def pytest_bdd_step_error(
    request: pytest.FixtureRequest,
    feature: object,
    scenario: object,
    step: object,
    step_func: Callable[..., object],
    step_func_args: dict[str, object],
    exception: BaseException,
) -> None:
    print("--- STEP FAILED\n")


def pytest_bdd_after_scenario(
    request: pytest.FixtureRequest, feature: object, scenario: object
) -> None:
    print("=================================================================\n")
